# Copyright (C) 2023, Roman V. M.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
Example video plugin that is compatible with Kodi 20.x "Nexus" and above
"""
import os
import sys
from urllib.parse import urlencode, parse_qsl
from lib import fetchVideosByGenre, fetchGenres, backend
import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
from xbmcvfs import translatePath

# Get the plugin url in plugin:// notation.
URL = sys.argv[0]
# Get a plugin handle as an integer number.
HANDLE = int(sys.argv[1])
# Get addon base path
ADDON_PATH = translatePath(Addon().getAddonInfo('path'))
ICONS_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'icons')
FANART_DIR = os.path.join(ADDON_PATH, 'resources', 'images', 'fanart')

# Public domain movies are from https://publicdomainmovie.net
# Here we use a hardcoded list of movies simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some website or online service.

VIDEOS1 = []
def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :return: plugin call URL
    :rtype: str
    """
    return '{}?{}'.format(URL, urlencode(kwargs))


def get_genres():
    """
    Gets genres
    :return: The list of video genres
    :rtype: list
    """
    VIDEOS1 = fetchGenres.getGenres()
    for genre in VIDEOS1:
        filename = str(genre['name']+'.png')
        genre['genre'] = genre['name']
        genre['icon'] = os.path.join(ICONS_DIR, filename )
        genre['fanart'] = os.path.join(FANART_DIR, 'Drama.jpg')
    
    return VIDEOS1


def get_videos(genre_index, page=1):
    genres = get_genres()
    genre = genres[genre_index]
    base_url = 'https://image.tmdb.org/t/p/original/'
    videos = fetchVideosByGenre.getVideos(str(genre["id"]), str(page))
    
    for video in videos:
        video['url'] = 'https://ia804707.us.archive.org/30/items/meet_john_doe_ipod/video_512kb.mp4'
        video['poster'] = base_url + video.get("poster_path", "")
        video['plot'] = video.get('overview', "No description available.")
        video['year'] = 0
    genre['movies'] = videos
    return genre

def list_genres():
    """
    Create the list of movie genres in the Kodi interface.
    """
    # Set plugin category. It is displayed in some skins as the name
    # of the current section.
    xbmcplugin.setPluginCategory(HANDLE, 'Public Domain Movies')
    # Set plugin content. It allows Kodi to select appropriate views
    # for this type of content.
    xbmcplugin.setContent(HANDLE, 'movies')
    # Get movie genres
    genres = get_genres()
    # Iterate through genres
    for index, genre_info in enumerate(genres):
        # Create a list item with a text label.
        list_item = xbmcgui.ListItem(label=genre_info['genre'])
        # Set images for the list item.
        list_item.setArt({'icon': genre_info['icon'], 'fanart': genre_info['fanart']})
        # Set additional info for the list item using its InfoTag.
        # InfoTag allows to set various information for an item.
        # For available properties and methods see the following link:
        # https://codedocs.xyz/xbmc/xbmc/classXBMCAddon_1_1xbmc_1_1InfoTagVideo.html
        # 'mediatype' is needed for a skin to display info for this ListItem correctly.
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('video')
        info_tag.setTitle(genre_info['genre'])
        info_tag.setGenres([genre_info['genre']])
        # Create a URL for a plugin recursive call.
        # Example: plugin://plugin.video.example/?action=listing&genre_index=0
        url = get_url(action='listing', genre_index=index)
        # is_folder = True means that this item opens a sub-list of lower level items.
        is_folder = True
        # Add our item to the Kodi virtual folder listing.
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, is_folder)
    # Add sort methods for the virtual folder items
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(HANDLE)


def list_videos(genre_index, page=1):
    """
    Create the list of playable videos in the Kodi interface with pagination.

    :param genre_index: the index of genre in the list of movie genres
    :type genre_index: int
    :param page: the current page of videos
    :type page: int
    """
    genre_info = get_videos(genre_index, page)
    xbmcplugin.setPluginCategory(HANDLE, genre_info['genre'])
    xbmcplugin.setContent(HANDLE, 'movies')
    videos = genre_info['movies']

    for video in videos:
        list_item = xbmcgui.ListItem(label=video['title'])
        list_item.setArt({'poster': video['poster']})
        info_tag = list_item.getVideoInfoTag()
        info_tag.setMediaType('movie')
        info_tag.setTitle(video['title'])
        info_tag.setGenres([genre_info['genre']])
        info_tag.setPlot(video['plot'])
        info_tag.setYear(video['year'])
        list_item.setProperty('IsPlayable', 'false')
        url = get_url(action='placeholder', video=video['url'], title=video['title'], id=video['id'])
        xbmcplugin.addDirectoryItem(HANDLE, url, list_item, False)

    # Add "Next Page" option
    next_page_item = xbmcgui.ListItem(label="Next Page")
    next_page_url = get_url(action='listing', genre_index=genre_index, page=page + 1)
    xbmcplugin.addDirectoryItem(HANDLE, next_page_url, next_page_item, True)

    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.addSortMethod(HANDLE, xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    xbmcplugin.endOfDirectory(HANDLE)


def placeholder_function(title,id):
    response = backend.addToRadarr(str(id))
    xbmcgui.Dialog().notification('Added to Library', f'Title: {title}', xbmcgui.NOTIFICATION_INFO, 5000)


def router(paramstring):
    """
    Router function to handle different actions based on the provided parameters.

    :param paramstring: Query string containing key-value pairs for routing actions.
                        Example: "action=listing&genre_index=1&page=2"
    :type paramstring: str
    """
    # Parse the query string into a dictionary of parameters.
    params = dict(parse_qsl(paramstring))
    
    # If no parameters are provided, list all available genres.
    if not params:
        list_genres()
    
    # If the 'action' parameter is 'listing', display a list of videos for the given genre and page.
    elif params['action'] == 'listing':
        # Get the page number from the parameters, defaulting to 1 if not specified.
        page = int(params.get('page', 1))
        # Get the genre index and list videos for that genre and page.
        list_videos(int(params['genre_index']), page)
    
    # If the 'action' parameter is 'play', play the video specified by the 'video' parameter.
    elif params['action'] == 'placeholder':
        placeholder_function(params['title'], params['id'])
    
    # If the 'action' parameter is invalid or missing, raise an error.
    else:
        raise ValueError(f'Invalid paramstring: {paramstring}!')


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])

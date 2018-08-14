import json
import sys
import sqlite3
import html
#Transfer from hw6 to public_html:
#_server.py, AJAXFunctions.js, music.html, scripts.js, style.css
#From cgi-bin to cgi-bin:
#song_interface.cgi - 755 permissions
#From server to server:
#hw6Server.py

# Part 1
def addSong(request, database):
    title = request['title']
    artist = request['artist']
    link = request['link']

    if title == "None" or artist == "None" or link == "None":
        # At least one of the fields was left empty. Do not add to the database
        return

    # Find a new ID for this song
    id = getNewID(database)

    # escape html for security
    title = html.escape(title)
    artist = html.escape(artist)
    link = html.escape(link)

    # TODO: Insert this song into the songs table
    #id INTEGER, title TEXT, artist TEXT, link Text
    database.execute("INSERT INTO songs VALUES (?, ?, ?, ?)", (id, title, artist, link))

# Part 2
def getAllSongs(database):
    # Format of songs dictionary:
    # {songID : [title, artist, YouTubeLink], songID : [title, artist, YoutubeLink],...}
    # Note: this function is not called by the website
    #.append() to
    songs = {}
    for row in database.execute('SELECT * FROM songs'):
        a = row
        for index in row:
            songID = row[0]
            title = row[1]
            artist = row[2]
            youtubeLink = row[3]

    #database.eecute("SELECT * FROM SONGS")
    #for row in database:
            #songs[row[0]] = [row[1], row[2], row[3]]
    #return json.dumps(songs)

    # TODO: populate the songs dictionary with all the songs in the songs table
            songDetails = [title, artist, youtubeLink]
            songs[songID] = songDetails
    return json.dumps(songs)


# Part 3
def setupDatabase():
    #Locally, use this line:
    #connection = sqlite3.connect('songDatabase.db')

    #On the CSE server, use this line:
    #connection = sqlite3.('/var/CSE113/alexurda/songDatabase.db')
    connection = sqlite3.connect('songDatabase.db')
    #connection = sqlite3.connect('/var/CSE113/alexurda/songDatabase.db')


    database = connection.cursor()
    database.execute("CREATE TABLE IF NOT EXISTS songs (id INTEGER, title TEXT, artist TEXT, link TEXT)")
    database.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER, review TEXT)")
    # TODO: Create a second table that will store the song reviews
    connection.commit()
    return connection
    #CREATE

def addReview(request, database):
    id = request["id"]
    review = request["review"]

    if id == "None" or review == "None":
        return getNewID(database)

    id = html.escape(id)
    review = html.escape(review)
    database.execute("INSERT INTO reviews VALUES (?, ?)", (id, review))
    #INSERT INTO
    # TODO: Insert the review into your reviews table

def getAllSongsAndReviews(database):
    # Format of songsAndReviews dictionary:
    # {songID : [title, artist, YouTubeLink, [review1, review2,...]],
    # songID : [title, artist, YoutubeLink, [review1, review2,...]],...}
    # .append()
    songsAndReviews = {}
    # TODO: populate the songsAndReviews dictionary with data from both SQL tables in the format above
    database.execute("SELECT * FROM songs")
    for row in database:
        songsAndReviews[row[0]] = [row[1], row[2], row[3], []]
    database.execute("SELECT * FROM reviews")
    for row in database:
        if row[0] in songsAndReviews.keys():
            songsAndReviews[row[0]][3].append(row[1])
    return json.dumps(songsAndReviews)
    #SELECT
    #for row in database.execute('SELECT * FROM table')
        #dictionaryName[row[0]]=[row[1], row[2], ...]
    #for row in database("reviews")
        #dictionaryName[row[0]][2] = row[1]
    #print(dictionaryName)
# The remaining code has been written for you.  Please do not make changes to it.

# Returns the next available ID to be used while inserting new songs
def getNewID(database):
    database.execute("SELECT MAX(id) FROM songs")
    maxID = database.fetchone()[0]
    newID = 0
    try:
        newID = maxID + 1
    except:
        pass
    return newID


def handleRequest(request):
    try:
        database = setupDatabase()

        if request["requestType"] == "addSong":
            addSong(request, database.cursor())
            response = "Song Submitted"
        elif request["requestType"] == "addReview":
            addReview(request, database.cursor())
            response = "Review Submitted"
        elif request["requestType"] == "getAllSongs":
            response = getAllSongs(database.cursor())
        elif request["requestType"] == "getAllSongsAndReviews":
            response = getAllSongsAndReviews(database.cursor())
        else:
            response = "Invalid Request Type"

        database.commit()
        database.close()
        return response
    except AttributeError as err:
        print(err)
    except:
        return sys.exc_info()[0]

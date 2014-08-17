Boardgame Webserver
====================

Introduction
------------

This flask application plays the boardgame described in the [boardgame-enumeration](../../../boardgame-enumeration) project. It uses its database to return a move for each incoming position request.

An online version is available [here](http://rockpaperscissors.flechtmann.net).

Getting started
---------------

[Flask](http://flask.pocoo.org) applications can be [run locally](http://flask.pocoo.org/docs/quickstart) or [deployed on a webserver](http://flask.pocoo.org/docs/deploying).

You just have to configure the moves.db filepath in server.py.

Parameters
----------

For a given position the application responds with the best move it finds. A move is represented by a number from 0 to 31. The number 0 means the white well goes forward, 1 means it goes to the top-left, 2 means left and so on. 8 means the white paper goes forward, 16 means the same for the white scissors and 24 for the white rock.

The application accepts requests like this:

    http://boardgame-webserver/a/b/c/d/e/f/g/h/i/j/k

Here the letters from a to k are used as:

| Letter | Used as                        |
|--------|--------------------------------|
| a      | Position of the white well     |
| b      | Position of the white paper    |
| c      | Position of the white scissors |
| d      | Position of the white rock     |
| e      | Position of the black well     |
| f      | Position of the black paper    |
| g      | Position of the black scissors |
| h      | Position of the black rock     |
| i      | Topdown flag                   |
| j      | Difficulty                     |
| k      | Mean flag                      |

Positions are Integers from 0 to 24. 0 means the piece has been taken. Fields are enumerated from the bottom left, going right and then upwards. This way the field in the bottom right is assigned number 4, top left 21 and top right 24.

Topdown is usually 0, meaning the application will return a move for the white player. When set to 1, a move for the black player is returned instead.

Difficulty is a number from 0 to 65. Results from the database higher than this setting are ignored.

Mean is usually 0. If set to 1, the AI tries to prolong the game as long as possible when winning.

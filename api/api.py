from flask import Blueprint, request
import sqlite3
import math

api_bp = Blueprint('api', __name__)


@api_bp.route('version', methods=['GET'])
def version():
    return "This is version 1"


@api_bp.route('drama', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def get_all_dramas():
    conn = sqlite3.connect('../dramalist.db')
    curr = conn.cursor()

    if request.method == 'GET':
        if request.args:
            name = request.args.get('name')
            row = curr.execute('SELECT name, episode, url FROM drama WHERE name = ?', (name.title(),)).fetchone()
            conn.close()
            return {"name": row[0], "episode": row[1], "url": row[2]}

        drama_list = []
        for row in curr.execute('SELECT name, episode, url FROM drama'):
            drama_list.append({"name": row[0], "episode": row[1], "url": row[2]})
        conn.close()
        return {"shows": drama_list}

    elif request.method == 'POST':
        data = request.form
        name = data.get('name')
        url = data.get('url')
        curr.execute("INSERT INTO drama(name,url) VALUES (?,?)", (name.title(), url))
        conn.commit()

    elif request.method == 'PATCH':
        name = request.args.get('name')
        episode = request.args.get('episode')
        curr.execute("UPDATE drama SET episode = ? WHERE name = ?", (episode, name.title()))
        conn.commit()

    elif request.method == 'DELETE':
        name = request.args.get('name')
        curr.execute("DELETE FROM drama WHERE name = ?", (name.title(),))
        conn.commit()

    conn.close()
    return 'OK', 201

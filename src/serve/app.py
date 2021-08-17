#!/usr/bin/env python

import os
import math
from markupsafe import escape
from collections import OrderedDict

import pygal
from flask import Flask, render_template, request, jsonify
from flask import flash, url_for, redirect, session
from flask_qrcode import QRcode

import dbops
import util

app = Flask(__name__)

app.secret_key = util.gen_secret_key()
app.json_encoder = dbops.JSONEncoder

qrcode = QRcode(app)

ITEMS_PER_PAGE = 20
MAIN_URL_HEAD = '127.0.0.1:5000'

COMPONENTS = OrderedDict([
    ('CPU', 'cpu'),
    ('Cooling System', 'cooler'),
    ('Motherboard', 'motherboard'),
    ('Memory', 'memory'),
    ('Storage Device', 'storage'),
    ('Case', 'case'),
    ('Power Supply Unit', 'psu'),
    ('Graphic Card', 'gpu'),
    ('Monitor', 'monitor'),
])


@app.route('/')
def index():
    return render_template('index.html', components=COMPONENTS)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    # save build
    if request.method == 'POST' and request.form.get('build_name') != None:
        build_url = util.gen_wishlist_url()
        while dbops.build_url_exists(build_url):
            build_url = util.gen_wishlist_url()

        return redirect(url_for(
            'saved_builds',
            build_url=build_url,
            build_name=request.form.get('build_name'),
        ))

    if 'wishlist' not in session or not session['wishlist']:
        return render_template('wishlist.html')

    total = util.total_build_cost(session['wishlist'])

    config = pygal.Config()
    config.human_readable = True
    config.style = pygal.style.LightGreenStyle

    chart = pygal.Pie(config, inner_radius=.4)
    chart.title = f"Total Build Cost: ₹{total}"

    for prod in session['wishlist']:
        chart.add(prod['title'], prod['price'])
    price_graph = chart.render_data_uri()

    return render_template('wishlist.html', price_graph=price_graph)


@app.route('/saved_build/<build_url>')
def saved_builds(build_url):
    if not dbops.build_url_exists(f"{MAIN_URL_HEAD}/saved_build/{build_url}"):
        if 'wishlist' not in session or not len(session['wishlist']) >= 1:
            return(render_template('404.html'))
        build_name = request.args.get('build_name')
        build_url = f'{MAIN_URL_HEAD}/saved_build/{build_url}'
        dbops.save_build(build_name, build_url, session['wishlist'])

    build_url = f'{MAIN_URL_HEAD}/saved_build/{build_url}'
    build = dbops.get_build_from_build_url(build_url)

    # price graph
    config = pygal.Config()
    config.human_readable = True
    config.style = pygal.style.LightGreenStyle

    # price history graph
    line_chart = pygal.Line(config)
    line_chart.title = "Build Price History"
    line_chart.x_labels = map(str, range(1, 90))

    total = util.total_build_cost(build['products'])

    chart = pygal.Pie(config, inner_radius=.4)
    chart.title = f"Total Build Cost: ₹{total}"

    for prod in build['products']:
        chart.add(prod['title'], prod['price'])
        line_chart.add(prod['title'], prod['price'])

    price_graph = chart.render_data_uri()
    history_graph = line_chart.render_data_uri()

    return render_template(
        'saved_build.html',
        build_url=build['build_url'],
        build_name=build['build_name'],
        price_graph=price_graph,
        history_graph=history_graph,
        build=build,
    )


@app.route('/component/<name>', methods=['GET', 'POST'])
def component(name):
    # generate a featdict
    if name == 'cpu':
        brands = dbops.get_category_key_vals('cpu', 'brand')
        cpu_series = dbops.get_category_key_vals('cpu', 'series')
        featdict = {'brand': brands, 'series': cpu_series}
    elif name == 'gpu':
        brands = dbops.get_category_key_vals('gpu', 'brand')
        gpu_series = dbops.get_category_key_vals('gpu', 'series')
        featdict = {'brand': brands, 'series': gpu_series}
    elif name == 'monitor':
        brands = dbops.get_category_key_vals('monitor', 'brand')
        panels = dbops.get_category_key_vals('monitor', 'panel')
        featdict = {'brand': brands, 'panel': panels}
    elif name == 'memory':
        brands = dbops.get_category_key_vals('memory', 'brand')
        speed = dbops.get_category_key_vals('memory', 'speed')
        memtype = dbops.get_category_key_vals('memory', 'type')
        capacity = dbops.get_category_key_vals('memory', 'capacity')
        featdict = {'brand': brands, 'speed': speed, 'type': memtype, 'capacity': capacity}
    else:
        brands = dbops.get_category_key_vals(name, 'brand')
        featdict = {'brand': brands}

    # generate all vendors
    vendors = dbops.get_category_key_vals(name, 'vendor')

    # check if the user has already set filters for this category
    sessionkey = f'{name}_filters'
    if sessionkey in session:
        hilodirection, queryfeatdict, queryvendors = session[sessionkey]
    else:
        # default values for queryfeatdict and queryvendors
        queryfeatdict = featdict
        queryvendors = vendors

    # get queryfeatdict and queryvendors (modified featdict and vendors from GET)
    if request.method == 'GET' and request.args.get('filter-submit') != None:
        queryfeatdict = {}
        queryvendors = []
        for arg in request.args:
            if arg.endswith('-check'):
                arg_split_list = arg.split('-')
                dbfield = arg_split_list[0]     # vendor, brand, type, capacity etc.
                dbfieldval = arg_split_list[1]  # vedant, itdepot, amd, etc.
                if dbfield == 'vendor':
                    queryvendors.append(dbfieldval)
                elif dbfield != 'price':
                    # Create queryfeatdict[dbfield] if it doesn't exist
                    _dbfield = queryfeatdict.setdefault(dbfield, [])
                    _dbfield.append(dbfieldval)
        if queryfeatdict == []:
            queryfeatdict = featdict
        if queryvendors == []:
            queryvendors = vendors
        session[sessionkey] = [1, 2, 3]         # placeholder values
        session[sessionkey][0] = 1              # hilodirection, TODO
        session[sessionkey][1] = queryfeatdict
        session[sessionkey][2] = queryvendors

    # product price order
    if request.method == 'POST' and request.form.get('hiloselect') != None:
        if request.form.get('hiloselect') == 'hilo':
            hilodirection = 'hilo'
        elif request.form.get('hiloselect') == 'lohi':
            hilodirection = 'lohi'
    else:
        hilodirection = 'lohi'
        
    # -1: high to low
    #  1: low to high
    if hilodirection == 'hilo':
        products = dbops.get_products(name, -1, queryfeatdict, queryvendors)
    elif hilodirection == 'lohi':
        products = dbops.get_products(name, 1, queryfeatdict, queryvendors)
    else:
        sys.exit("Error")

    # get pageno
    if request.method == 'GET' and request.args.get('pageno') != None:
        pageno = int(request.args.get('pageno'))
    else:
        pageno = 1

    # get total number of pages to be displayed
    numpages = math.ceil(len(products) / ITEMS_PER_PAGE)

    # gives the products to be displayed on page {pageno}
    data = products[pageno * ITEMS_PER_PAGE - ITEMS_PER_PAGE : pageno * ITEMS_PER_PAGE]

    return render_template(
        'component.html',
        name=name,
        data=data,
        pagelen=ITEMS_PER_PAGE,
        pageno=pageno,
        components=COMPONENTS,
        numpages=numpages,
        hilodirection=hilodirection,
        featdict=featdict,
    )


@app.route('/_add_to_wishlist/<product_id>')
def add_to_wishlist(product_id):
    # Create session['wishlist'] if it doesn't exist
    wishlist = session.setdefault('wishlist', [])

    # Ensure product is not already in the wishlist
    for prod in wishlist:
        if prod['_id'] == product_id:
            flash("Product has already been added")
            return jsonify(message="Failed to add")

    product = dbops.get_product_from_id(product_id)
    wishlist.append(product)
    session.modified = True
    return jsonify(newtext="Remove from Wishlist", newid=f"remove-{product_id}")


@app.route('/_remove_from_wishlist/<product_id>')
def remove_from_wishlist(product_id):
    # Ensure session['wishlist'] exists
    if 'wishlist' not in session:
        return "Failed to Remove"

    session['wishlist'] = [prod for prod in session['wishlist'] if not (prod['_id']) == product_id]
    session.modified = True
    return jsonify(newtext="Add to Wishlist", newid=f"add-{product_id}")


@app.route('/_wishlist_toggle/<product_id>')
def wishlist_toggle(product_id):
    if 'wishlist' not in session:           # definitely add
        wishlist = session.setdefault('wishlist', [])
        product = dbops.get_product_from_id(product_id)
        wishlist.append(product)
        session.modified = True
        return jsonify(
            message="change button to remove",
            newbuttonid=f"remove-{product_id}",
            newbuttonclass="btn-remove",
            newbuttontext="remove from wishlist",
        )

    else:                                   # maybe add, maybe remove
        wishlist = session['wishlist']
        for prod in wishlist:
            if prod['_id'] == product_id:   # definitely remove
                session['wishlist'] = [
                    prod for prod in session['wishlist'] if not (prod['_id']) == product_id
                ]
                session.modified = True
                return jsonify(
                    message="change button to add",
                    newbuttonid=f"add-{product_id}",
                    newbuttonclass="btn-add",
                    newbuttontext="add to wishlist",
                )
        # definitely add
        product = dbops.get_product_from_id(product_id)
        wishlist.append(product)
        session['wishlist'] = sorted(session['wishlist'], key=lambda k: k['url']) 
        session.modified = True
        return jsonify(
            message="change button to remove",
            newbuttonid=f"remove-{product_id}",
            newbuttonclass="btn-remove",
            newbuttontext="remove from wishlist",
        )


@app.route('/comparison')
def comparison():
    return render_template('comparison.html')


@app.route('/_comparison/<product_id>')
def comparison_toggle(product_id):
    product = dbops.get_product_from_id(product_id)

    if product['vendor'] not in ['itdepot', 'mdcomputer', 'vedant']:
        flash(f"Comparison not available for vendor {product['vendor']}")
        return "incompatible vendor"

    if 'comparison' not in session: # definitely add
        comparison = session.setdefault('comparison', [])
        comparison.append(product)
        session.modified = True
        newbuttontext = "remove"
        return jsonify(newbuttontext=newbuttontext)

    else:   # maybe add, maybe remove
        comparison = session['comparison']
        for prod in comparison:
            if prod['_id'] == product_id:  # definitely remove
                session['comparison'] = [
                    prod for prod in session['comparison'] if not (prod['_id']) == product_id
                ]
                session.modified = True
                return jsonify(newbuttontext="compare")

        # definitely add
        if len(comparison) >= 2:
            flash("Two elements already added for comparison.  Remove one of them if you want to add another.")
            os.system("echo two added")
            return "too many products"
        comparison.append(product)
        session.modified = True
        return jsonify(newbuttontext="compare")


@app.route('/_comparison_remove_all')
def comparison_remove_all():
    del session['comparison']
    session.modified = True
    return redirect(url_for('comparison'))


if __name__ == '__main__':
    app.run(debug=True)

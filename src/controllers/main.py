from flask import Blueprint, render_template, abort, redirect, url_for, jsonify, request, make_response,stream_with_context
from datetime import datetime
from flask_login import login_required, current_user
from src.models.user import User
from src.models.permission import Permission
import time
import csv
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from random import randint, choice
from werkzeug.datastructures import Headers
from werkzeug.wrappers import Response


main = Blueprint('main', __name__)

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)



@main.route('/')
@main.route('/home')
def home():
    data_list = []
    data = None
    P_TYPE = ["PROP_INSURANCE", "AUTO_INSURANCE"]
    LC_STATUS = ["TERMINATED", "EFFECTIVE"]
    show_data=request.args.get('show_data')
    if show_data:
       for i in range(50):
             data = { "USAA_PARTY_TD_ID":"{}".format(random_digits(8)),
                      "USAA_PD_ID_TYPE_CD":"USAA",
                      "S_ARRANGEMENT_ID":"{}".format(random_digits(15)),
                      "ORIG_EFFECTIVE_DT":"2017-10-{}{}".format(randint(0,2),randint(1,9)),
                      "P_ARRANGEMENT_TYPE_CD": choice(P_TYPE),
                      "LC_STATUS_CD": choice(LC_STATUS),
                      "LC_STATUS_STR_DT": "2017-10-{}{}".format(randint(0,2),randint(1,9))
                     }
             data_list.append(data)
    if current_user.is_anonymous:
        return redirect(url_for('main.splash'))
    return render_template('home.html', current_time=datetime.utcnow(), show_data=show_data, data=data_list)

@main.route('/splash')
def splash():
    return render_template('splash.html', current_time=datetime.utcnow())

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)





@main.route('/splash2')
def splash2():
    return render_template('query_loader.html')



@main.route('/dataload', methods=['POST'])
def process():
    time.sleep(4)
    return redirect(url_for('main.home', show_data='True'))



@main.route('/save_query', methods=['POST'])
def save_query():
    time.sleep(4)
    return redirect(url_for('main.home'))


def random_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


@main.route('/download')
def download_csv():
    data = None
    data_list = []
    P_TYPE = ["PROP_INSURANCE", "AUTO_INSURANCE"]
    LC_STATUS = ["TERMINATED", "EFFECTIVE"]
    for i in range(50):
        data = {"USAA_PARTY_TD_ID": "{}".format(random_digits(8)),
                "USAA_PD_ID_TYPE_CD": "USAA",
                "S_ARRANGEMENT_ID": "{}".format(random_digits(15)),
                "ORIG_EFFECTIVE_DT": "2017-10-{}{}".format(randint(0, 2), randint(1, 9)),
                "P_ARRANGEMENT_TYPE_CD": choice(P_TYPE),
                "LC_STATUS_CD": choice(LC_STATUS),
                "LC_STATUS_STR_DT": "2017-10-{}{}".format(randint(0, 2), randint(1, 9))
                }
        data_list.append(data)

    def generate():
        data = StringIO()
        w = csv.writer(data)

        # write header
        w.writerow(("USAA_PARTY_TD_ID" , "USAA_PD_ID_TYPE_CD", "S_ARRANGEMENT_ID",
                    "ORIG_EFFECTIVE_DT", "P_ARRANGEMENT_TYPE_CD",  "LC_STATUS_CD",  "LC_STATUS_STR_DT"
                    ))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        """
        for item in data_list:
            w.writerow((
                item[0],
                item[1]
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)
        """

    # add a filename
    headers = Headers()
    headers.set('Content-Disposition', 'attachment', filename='data.csv')

    return Response(
        stream_with_context(generate()),
        mimetype='text/csv', headers=headers
    )



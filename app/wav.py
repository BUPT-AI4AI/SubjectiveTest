""" Client App """

import os
from flask import Blueprint, render_template

wav_bp = Blueprint('wav_app', __name__,
                      url_prefix='',
                      static_url_path='',
                      static_folder='./resource/',
                      )

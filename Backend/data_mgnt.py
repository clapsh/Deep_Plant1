# 엑셀 파일 업로드
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from auth import login_required

bp = Blueprint('data_mgnt', __name__, url_prefix='/data')
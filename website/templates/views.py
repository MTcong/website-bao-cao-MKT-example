from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
import json
from .models import *
from datetime import *
from sqlalchemy import or_, and_
from dateutil.relativedelta import relativedelta


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@views.route('/bank', methods=['GET', 'POST'])
@login_required
def bank():

    if request.method == 'POST':
        form_id = request.form.get('form_id')

        if form_id == 'form-add':
            name = request.form.get('name')
            shortName = request.form.get('shortName')
            code = request.form.get('code')
            bin = request.form.get('bin')
            swift_code = request.form.get('swift_code')

            new_bank = Bank(name=name, shortName=shortName, code=code, bin=bin, swift_code=swift_code)

            db.session.add(new_bank)
            db.session.commit()
            flash("Thêm ngân hàng mới thành công!", category='success')

        if form_id == 'form-edit':
            id = request.form.get('edit-id')
            bank = Bank.query.get(id)
            
            if bank:
                bank.name = request.form.get('edit-name')
                bank.shortName = request.form.get('edit-shortName')
                bank.code = request.form.get('edit-code')
                bank.bin = request.form.get('edit-bin')
                bank.swift_code = request.form.get('edit-swift_code')

                db.session.commit()
                flash("Chỉnh sửa thông tin ngân hàng thành công!", category='success')
            else:
                flash("Ngân hàng không còn tồn tại trên hệ thống.", category='error')

    banks = Bank.query.all()
    bank_list = []
    for bank in banks:
        bank_data = {
            'id': bank.id,
            'name': bank.name,
            'code': bank.code,
            'bin': bank.bin,
            'shortName': bank.shortName,
            'logo': bank.logo,
            'swift_code': bank.swift_code
        }
        bank_list.append(bank_data)

    return render_template('bank.html', user=current_user, bank_list=bank_list)


@views.route('/bank/delete/<int:id>', methods=['POST'])
@login_required
def delete_bank(id):
    bank = Bank.query.get(id)
    if bank:
        db.session.delete(bank)
        db.session.commit()
        flash("Xoá ngân hàng thành công!", category='success')
    else:
        flash("Ngân hàng không còn tồn tại trên hệ thống.", category='error')
    return redirect(url_for('views.bank'), user=current_user)


@views.route('/staff', methods=['GET', 'POST'])
@login_required
def staff():
    if request.method == 'POST':
        form_id = request.form.get('form_id')

        if form_id == 'form-add':
            name = request.form.get('name')
            address = request.form.get('address')
            phone = request.form.get('phone')
            cccd = request.form.get('cccd')
            email = request.form.get('email')
            dob_str = request.form.get('dob')

            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

            new_staff = User(name=name, address=address, phone=phone, cccd=cccd, email=email, dob=dob, role="staff", password=generate_password_hash('A@123456'))

            db.session.add(new_staff)
            db.session.commit()
            flash("Thêm nhà cung cấp mới thành công!", category='success')

        if form_id == 'form-edit':
            id = request.form.get('edit-id')
            staff = User.query.get(id)
            
            if staff:
                staff.name = request.form.get('edit-name')
                staff.address = request.form.get('edit-address')
                staff.phone = request.form.get('edit-phone')
                staff.cccd = request.form.get('edit-cccd')
                staff.email = request.form.get('edit-email')

                dob_str = request.form.get('edit-dob')
                
                staff.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

                db.session.commit()
                flash("Chỉnh sửa thông tin nhà cung cấp thành công!", category='success')
            else:
                flash("Nhà cung cấp không còn tồn tại trên hệ thống.", category='error')

    staffs = User.query.filter_by(role='staff').all()
    staff_list = []
    for staff in staffs:
        staff_data = {
            'id': staff.id,
            'name': staff.name,
            'email': staff.email,
            'phone': staff.phone,
            'address': staff.address,
            'cccd': staff.cccd,
            'dob': staff.dob.strftime("%d/%m/%Y")
        }
        staff_list.append(staff_data)

    return render_template('staff.html', user=current_user, staff_list=staff_list)


@views.route('/staff/delete/<int:id>', methods=['POST'])
@login_required
def delete_staff(id):
    staff = User.query.get(id)
    if staff:
        db.session.delete(staff)
        db.session.commit()
        flash("Xoá nhân viên thành công!", category='success')
    else:
        flash("Nhân viên không còn tồn tại trên hệ thống.", category='error')
    return redirect(url_for('views.staff'), user=current_user)


@views.route('/bao-cao-gio', methods=['GET'])
@login_required
def bcgio():
    today = date.today()
    return redirect(url_for(f'views.bao_cao_gio', y=today.year, m=today.month, d=today.day))


@views.route('/bao-cao-gio/<int:y>-<int:m>-<int:d>', methods=['GET', 'POST'])
@login_required
def bao_cao_gio(y, m, d):

    now = datetime.now()
    ddate = datetime.strptime(f'{y}-{m}-{d}', '%Y-%m-%d').date()
    time_1130 = datetime.combine(ddate, datetime.min.time()).replace(hour=11, minute=30, second=0, microsecond=0)
    time_1700 = datetime.combine(ddate, datetime.min.time()).replace(hour=17, minute=0, second=0, microsecond=0)

    if now > time_1700:
        render_table = 0
    elif now > time_1130:
        render_table = 1
    else:
        render_table = 2

    staffs = User.query.all()
    for staff in staffs:
        if Hour_report.query.filter(and_( Hour_report.user_id == staff.id, or_(Hour_report.time == time_1130, Hour_report.time == time_1700))).all():
            continue
        else:
            user_id = staff.id
            new_report_1130 = Hour_report(user_id=user_id, time=time_1130)
            db.session.add(new_report_1130)
            new_report_1700 = Hour_report(user_id=user_id, time=time_1700)
            db.session.add(new_report_1700)
            db.session.commit()

    if request.method == 'POST':
        form_id = request.form.get('form_id')

        if form_id == 'form-1130':
            user_id = request.form.get('user_id')
            report = Hour_report.query.filter_by(user_id=user_id, time=time_1130).first()
            if report:
                report.cost = request.form.get(f'cost')
                report.phoneNumber = request.form.get(f'phoneNumber')
                report.revenue = request.form.get(f'revenue')
                db.session.commit()
            flash("Báo cáo thành công!", category='success')

        if form_id == 'form-1700':
            user_id = request.form.get('user_id')
            report = Hour_report.query.filter_by(user_id=user_id, time=time_1700).first()
            if report:
                report.cost = request.form.get(f'cost')
                report.phoneNumber = request.form.get(f'phoneNumber')
                report.revenue = request.form.get(f'revenue')
                db.session.commit()
            flash("Báo cáo thành công!", category='success')

    staffs = User.query.all()
    staff_list = []
    for staff in staffs:
        staff_data = {
            'id': staff.id,
            'name': staff.name
        }
        staff_list.append(staff_data)
    
    reports = Hour_report.query.filter(or_(Hour_report.time == time_1130, Hour_report.time == time_1700)).all()
    report_list = []

    for report in reports:
        report_data = {
            'user_id': report.user_id,
            'time': '1130' if report.time==time_1130 else '1700',
            'cost': f'{report.cost:,}',
            'phoneNumber': f'{report.phoneNumber:,}',
            'costPerPhone': f'{int(round(report.cost/report.phoneNumber, 0) if report.phoneNumber != 0 else 0):,}',
            'revenue': f'{report.revenue:,}',
            'cpqc': f'{round(report.cost/report.revenue * 100 if report.revenue != 0 else 0, 2):,}',
            'roat': f'{round(report.revenue/report.cost if report.cost != 0 else 0, 2):,}'
        }
        report_list.append(report_data)

    return render_template('bao-cao-gio.html', user=current_user, staff_list=staff_list, report_list=report_list, ddate=ddate, render_table=render_table)


@views.route('/bao-cao-bai-test', methods=['GET'])
@login_required
def bcbtest():
    today = date.today()
    one_month_before = today - relativedelta(months=1)
    return redirect(url_for(f'views.bao_cao_gio', yb=one_month_before.year, mb=one_month_before.month, dbb=one_month_before.day, y=today.year, m=today.month, d=today.day))


@views.route('/bao-cao-bai-test/<int:yb>-<int:mb>-<int:db>-<int:y>-<int:m>-<int:d>', methods=['GET', 'POST'])
@login_required
def bao_cao_bai_test(yb, mb, dbb, y, m, d):
    date1 = datetime.strptime(f'{yb}-{mb}-{dbb}', '%Y-%m-%d').date()
    date2 = datetime.strptime(f'{y}-{m}-{d}', '%Y-%m-%d').date()

    if request.method == 'POST':
        form_id = request.form.get('form_id')

        if form_id == 'form-1130':
            # user_id = request.form.get('user_id')
            # report = Hour_report.query.filter_by(user_id=user_id, time=time_1130).first()
            # if report:
            #     report.cost = request.form.get(f'cost')
            #     report.phoneNumber = request.form.get(f'phoneNumber')
            #     report.revenue = request.form.get(f'revenue')
            #     db.session.commit()
            flash("Báo cáo thành công!", category='success')

        if form_id == 'form-1700':
            # user_id = request.form.get('user_id')
            # report = Hour_report.query.filter_by(user_id=user_id, time=time_1700).first()
            # if report:
            #     report.cost = request.form.get(f'cost')
            #     report.phoneNumber = request.form.get(f'phoneNumber')
            #     report.revenue = request.form.get(f'revenue')
            #     db.session.commit()
            flash("Báo cáo thành công!", category='success')

    staffs = User.query.all()
    staff_list = []
    for staff in staffs:
        staff_data = {
            'id': staff.id,
            'name': staff.name
        }
        staff_list.append(staff_data)
    
    posts = Post.query.filter(Post.time.between(date1, date2)).all()
    post_list = []

    for post in posts:
        post_data = {
            'user_id': post.user_id,
            'link': post.link,
            'type': post.type,
            'content': post.content,
            'budget': post.budget,
            'cpm': post.cpm,
            'cpc': post.cpc,
            'ctr': post.ctr,
            'cpa': post.cpa,
            'cpPerCpa': f'{int(round(post.budget/post.cpa, 0) if post.cpa != 0 else 0):,}',
            'order': post.order,
            'cpPerOrder': f'{int(round(post.budget/post.order, 0) if post.order != 0 else 0):,}',
            'review': post.review,
        }
        post_list.append(post_data)

    return render_template('bao-cao-bai-test.html', user=current_user, staff_list=staff_list, post_list=post_list)
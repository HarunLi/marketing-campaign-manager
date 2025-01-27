from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from app.models import Campaign, Order, Prize
from datetime import datetime, timedelta
import traceback
from flask import render_template, redirect, url_for
from app.forms import CampaignForm

bp = Blueprint('main', __name__)

@bp.route('/init_data')
def init_data():
    try:
        # 清除现有数据
        db.session.query(Order).delete()
        db.session.query(Prize).delete()
        db.session.query(Campaign).delete()

        # 创建测试活动
        campaign1 = Campaign(
            name='夏季促销活动',
            description='夏季全场8折优惠',
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
            status='进行中'
        )
        campaign2 = Campaign(
            name='新品推广',
            description='新品上市，限时优惠',
            start_date=datetime.now() + timedelta(days=15),
            end_date=datetime.now() + timedelta(days=45),
            status='未开始'
        )

        # 添加到数据库
        db.session.add(campaign1)
        db.session.add(campaign2)
        db.session.commit()

        # 创建测试订单
        order1 = Order(
            campaign_id=campaign1.id,
            customer_name='张三',
            order_date=datetime.now(),
            total_amount=500.00
        )
        order2 = Order(
            campaign_id=campaign1.id,
            customer_name='李四',
            order_date=datetime.now(),
            total_amount=750.50
        )

        # 创建测试奖品
        prize1 = Prize(
            campaign_id=campaign1.id,
            name='限量T恤',
            description='夏季促销特别款',
            quantity=100
        )
        prize2 = Prize(
            campaign_id=campaign2.id,
            name='智能音箱',
            description='新品推广赠品',
            quantity=50
        )

        # 添加到数据库
        db.session.add_all([order1, order2, prize1, prize2])
        db.session.commit()

        return '测试数据初始化完成'
    except Exception as e:
        db.session.rollback()
        error_trace = traceback.format_exc()
        print(error_trace)
        return f"初始化数据失败：{str(e)}\n{error_trace}", 500

@bp.route('/')
def index():
    try:
        campaigns = Campaign.query.all()
        total_campaigns = len(campaigns)
        total_orders = Order.query.count()
        total_prizes = Prize.query.count()
        return render_template('index.html', 
                               campaigns=campaigns, 
                               total_campaigns=total_campaigns,
                               total_orders=total_orders,
                               total_prizes=total_prizes)
    except Exception as e:
        error_trace = traceback.format_exc()
        print(error_trace)
        return f"渲染页面失败：{str(e)}\n{error_trace}", 500

@bp.route('/campaigns')
def campaigns():
    campaigns = Campaign.query.all()
    return render_template('campaigns.html', campaigns=campaigns)

@bp.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@bp.route('/prizes')
def prizes():
    prizes = Prize.query.all()
    return render_template('prizes.html', prizes=prizes)

@bp.route('/campaign/<int:campaign_id>')
def campaign_detail(campaign_id):
    try:
        campaign = Campaign.query.get_or_404(campaign_id)
        # 获取与该活动相关的订单和奖品
        orders = Order.query.filter_by(campaign_id=campaign_id).all()
        prizes = Prize.query.filter_by(campaign_id=campaign_id).all()

        return render_template('campaign_detail.html',
                               campaign=campaign,
                               orders=orders,
                               prizes=prizes)
    except Exception as e:
        error_trace = traceback.format_exc()
        print(error_trace)
        return f"获取活动详情失败：{str(e)}\n{error_trace}", 500


@bp.route('/campaign/<int:campaign_id>/edit', methods=['GET', 'POST'])
def edit_campaign(campaign_id):
    try:
        campaign = Campaign.query.get_or_404(campaign_id)
        form = CampaignForm(obj=campaign)

        if form.validate_on_submit():
            campaign.name = form.name.data
            campaign.description = form.description.data
            campaign.start_date = form.start_date.data
            campaign.end_date = form.end_date.data
            campaign.status = form.status.data

            db.session.commit()
            return redirect(url_for('main.campaign_detail', campaign_id=campaign.id))

        return render_template('edit_campaign.html', form=form, campaign=campaign)
    except Exception as e:
        error_trace = traceback.format_exc()
        print(error_trace)
        return f"编辑活动失败：{str(e)}\n{error_trace}", 500


@bp.route('/campaign/<int:campaign_id>/delete', methods=['POST'])
def delete_campaign(campaign_id):
    try:
        campaign = Campaign.query.get_or_404(campaign_id)

        # 级联删除相关的订单和奖品
        Order.query.filter_by(campaign_id=campaign_id).delete()
        Prize.query.filter_by(campaign_id=campaign_id).delete()

        db.session.delete(campaign)
        db.session.commit()

        return redirect(url_for('main.campaigns'))
    except Exception as e:
        db.session.rollback()
        error_trace = traceback.format_exc()
        print(error_trace)
        return f"删除活动失败：{str(e)}\n{error_trace}", 500


@bp.route('/create_campaign', methods=['GET', 'POST'])
def create_campaign():
    form = CampaignForm()
    if form.validate_on_submit():
        campaign = Campaign(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data
        )
        try:
            db.session.add(campaign)
            db.session.commit()
            return redirect(url_for('main.campaign_detail', campaign_id=campaign.id))
        except Exception as e:
            db.session.rollback()
            error_trace = traceback.format_exc()
            print(error_trace)
            form.name.errors.append(f"创建活动失败：{str(e)}")

    return render_template('create_campaign.html', form=form)
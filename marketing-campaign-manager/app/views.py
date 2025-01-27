from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import Campaign

@app.route('/')
def campaigns():
    campaigns = Campaign.query.all()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/campaign/<int:campaign_id>')
def campaign_detail(campaign_id):
    campaign = Campaign.query.get_or_404(campaign_id)
    return render_template('campaign_detail.html', campaign=campaign)
# -*- coding: utf-8 -*-
from spike_system.model import db
from datetime import datetime


# 用户
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    addr = db.Column(db.String(255), nullable=True)
    is_ok = db.Column(db.Integer, default=1)
    img_url = db.Column(db.Text, default="http://www.2cto.com/uploadfile/2014/0321/20140321081401358.jpg",
                        nullable=True)
    scores = db.Column(db.Integer, default=0)  # 用户积分
    identity = db.Column(db.Integer, default=0)  # 0普通用户，1会员
    shop_time = db.Column(db.DateTime)

# 一级类别

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.String(50), primary_key=True)
    cname = db.Column(db.String(255), nullable=False)

    def category_json(self):
        category_json = {}
        category_json["id"] = self.id
        category_json["cname"] = self.cname
        return category_json


# 二级类别
class CategorySecond(db.Model):
    __tablename__ = 'category_second'
    id = db.Column(db.String(50), primary_key=True)
    csname = db.Column(db.String(255), nullable=False)
    cid = db.Column(db.String(50), db.ForeignKey('category.id', ondelete='cascade'))
    category = db.relationship("Category", backref=db.backref('categoryseconds'))


# 商品
class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.String(50), primary_key=True)
    pname = db.Column(db.String(255), nullable=False)
    old_price = db.Column(db.Float, nullable=False)
    new_price = db.Column(db.Float, nullable=False)
    images = db.Column(db.Text)
    pDesc = db.Column(db.Text)
    head_img = db.Column(db.Text)
    is_hot = db.Column(db.Integer, default=0)  # 0不是热卖品，1热卖品 2推广品
    is_sell = db.Column(db.Integer, default=1)  # 0销完 1在售
    is_pass = db.Column(db.Integer, default=0)  # 0正在审核 1审核未通过 2 审核通过
    pdate = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    click_count = db.Column(db.Integer, default=0)
    counts = db.Column(db.Integer, nullable=False)
    love_user = db.Column(db.Text)  # 喜爱的人
    uid = db.Column(db.String(50), db.ForeignKey("user.id", ondelete='cascade'))
    user = db.relationship("User", backref=db.backref('products', order_by=pdate.desc()))
    csid = db.Column(db.String(50), db.ForeignKey("category_second.id", ondelete='cascade'))
    categorysecond = db.relationship("CategorySecond", backref=db.backref("products", order_by=pdate.desc()))

    def product_json(self):
        product_json = dict()
        product_json["id"] = self.id
        product_json["pname"] = self.pname
        product_json["images"] = self.images.split('@')[0]
        product_json["counts"] = self.counts
        product_json["old_price"] = self.old_price
        product_json["new_price"] = self.new_price
        return product_json

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, TIMESTAMP, text
# from app.db.seconfig.database import Base
from app.db.base import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from sqlalchemy.sql import func

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum,
    Boolean,
    ForeignKey,
    JSON,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


# class Blog(Base):
#     __tablename__ = 'blogs'

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     body = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))

#     creator = relationship("User", back_populates="blogs")


# class User(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String)
#     password = Column(String)

#     blogs = relationship('Blog', back_populates="creator")


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    # created_at = Column(DateTime(timezone=True), default=func.now())
    created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, onupdate=func.utcnow())
    updated_at = Column(DateTime, default=datetime.now,
                        onupdate=datetime.utcnow)

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

    def __hash__(self):
        return hash(self.id)

    def __init__(self):
        self._q = None
        self._session = None

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        """
        테이블 데이터 적재 전용 함수
        :param session:
        :param auto_commit: 자동 커밋 여부
        :param kwargs: 적재 할 데이터
        :return:
        """
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        return obj

    @classmethod
    def get(cls, **kwargs):
        """
        Simply get a Row
        :param kwargs:
        :return:
        """
        session = next(db.session())
        query = session.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception(
                "Only one row is supposed to be returned, but got more than one.")
        result = query.first()
        session.close()
        return result

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        """
        Simply get a Row
        :param session:
        :param kwargs:
        :return:
        """
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            if len(key) > 2:
                raise Exception("No 2 more dunders")
            col = getattr(cls, key[0])
            if len(key) == 1:
                cond.append((col == val))
            elif len(key) == 2 and key[1] == 'gt':
                cond.append((col > val))
            elif len(key) == 2 and key[1] == 'gte':
                cond.append((col >= val))
            elif len(key) == 2 and key[1] == 'lt':
                cond.append((col < val))
            elif len(key) == 2 and key[1] == 'lte':
                cond.append((col <= val))
            elif len(key) == 2 and key[1] == 'in':
                cond.append((col.in_(val)))

        obj = cls()
        if session:
            obj._session = session
            obj._sess_served = True
        else:
            obj._session = next(db.session())
            obj._sess_served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls

    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = self._q.order_by(
                col.asc()) if is_asc else self._q.order_by(col.desc())
        return self

    def update(self, sess: Session = None, auto_commit: bool = False, **kwargs):
        cls = self.cls_attr()
        if sess:
            query = sess.query(cls)
        else:
            sess = next(db.session())
            query = sess.query(cls)
        self.close()
        return query.update(**kwargs)

    def first(self):
        result = self._q.first()
        self.close()
        return result

    def delete(self, auto_commit: bool = False, **kwargs):
        self._q.delete()
        if auto_commit:
            self._session.commit()
        self.close()

    def all(self):
        result = self._q.all()
        self.close()
        return result

    def count(self):
        result = self._q.count()
        self.close()
        return result

    def dict(self, *args: str):
        q_dict = {}
        for c in self.__table__.columns:
            if c.name in args:
                q_dict[c.name] = getattr(self, c.name)

        return q_dict

    def close(self):
        if self._sess_served:
            self._session.commit()
            self._session.close()
        else:
            self._session.flush()


class Discussion(Base, BaseMixin):
    __tablename__ = 'discussions'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    progress = Column(String, nullable=True)
    status = Column(String, nullable=True)

    discussion_topic = Column(String(length=3000), nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class Incident(Base, BaseMixin):
    __tablename__ = 'incidents'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    shift_start_date = Column(DateTime, default=None)
    shift_type = Column(String, nullable=True)

    level_1_engineer1 = Column(String, nullable=True)
    level_1_engineer2 = Column(String, nullable=True)
    level_2_engineers = Column(String, nullable=True)
    how_to_share = Column(String, nullable=True)

    event = Column(String, nullable=True)
    action = Column(String(length=3000), nullable=True)
    status = Column(String, nullable=True)
    ticket_no = Column(String, nullable=True)
    escalated_to_l3 = Column(String, nullable=True)
    comment = Column(String(length=3000), nullable=True)

    occurred_at = Column(DateTime, default=None, nullable=True)
    acknowledged_at = Column(DateTime, default=None, nullable=True)
    propogated_at = Column(DateTime, default=None, nullable=True)
    resolved_at = Column(DateTime, default=None, nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)

    # time_to_acknowledge = Column(Integer, default=None) # acknowledged_at - occurred_at
    # time_to_propogated = Column(Integer, default=None)  # propogated_at - acknowledged_at


class Issue(Base, BaseMixin):
    __tablename__ = 'issues'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    progress = Column(String, nullable=True)
    status = Column(String, nullable=True)

    title = Column(String, nullable=True)
    description = Column(String(length=3000), nullable=True)
    action = Column(String(length=3000), nullable=True)

    occurred_at = Column(DateTime, default=datetime.now)
    resolved_at = Column(DateTime, default=None, nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class Problem(Base, BaseMixin):
    __tablename__ = 'problems'

    # status = Column(Enum("active", "deleted", "blocked"), default="active")
    # email = Column(String(length=255), nullable=True)
    # pw = Column(String(length=3000), nullable=True)
    # name = Column(String(length=255), nullable=True)
    # phone_number = Column(String(length=30), nullable=True, unique=True)
    # profile_img = Column(String(length=1000), nullable=True)
    # sns_type = Column(Enum("FB", "G", "K"), nullable=True)
    # marketing_agree = Column(Boolean, nullable=True, default=True)

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    progress = Column(String, nullable=True)
    status = Column(String, nullable=True)
    impact = Column(String, nullable=True)

    title = Column(String, nullable=True)
    description = Column(String(length=3000), nullable=True)
    action = Column(String(length=3000), nullable=True)
    person_in_charge = Column(String, nullable=True)  # Engineer
    ticket_no = Column(String, nullable=True)

    rca_desc = Column(String(length=3000), nullable=True)
    review_desc = Column(String(length=3000), nullable=True)

    occurred_at = Column(DateTime, default=datetime.now)
    reviewed_at = Column(DateTime, default=None)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class Change(Base, BaseMixin):
    __tablename__ = 'changes'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    progress = Column(String, nullable=True)
    status = Column(String, nullable=True)

    ticket_no = Column(String, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String(length=3000), nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class Request(Base, BaseMixin):
    __tablename__ = 'requests'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    progress = Column(String, nullable=True)
    status = Column(String, nullable=True)

    ticket_no = Column(String, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String(length=3000), nullable=True)
    work_type = Column(String, nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class Capacity(Base, BaseMixin):
    __tablename__ = 'capacities'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    progress = Column(String, nullable=True)
    status = Column(String, nullable=True)

    category = Column(String, nullable=True)
    ticket_no = Column(String, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String(length=3000), nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class Backup(Base, BaseMixin):
    __tablename__ = 'backups'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    progress = Column(String, nullable=True)
    status = Column(String, nullable=True)

    db_type = Column(String, nullable=True)
    instance_name = Column(String, nullable=True)
    instance_ip = Column(String, nullable=True)
    freq_full_archive = Column(String, nullable=True)
    comment = Column(String(length=3000), nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class Instance(Base, BaseMixin):
    __tablename__ = 'instances'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    status = Column(String, nullable=True)
    count = Column(Integer, nullable=False)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class Kubernetes(Base, BaseMixin):
    __tablename__ = 'kubernetes'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    status = Column(String, nullable=True)
    cluster_name = Column(String, nullable=True)
    node_type = Column(String, nullable=True)
    node_name = Column(String, nullable=True)
    node_ips = Column(String, nullable=True)
    api_vip = Column(String, nullable=True)
    flavor = Column(String, nullable=True)
    network_zone = Column(String, nullable=True)
    contacts = Column(String, nullable=True)
    k8s_version = Column(String, nullable=True)
    monitoring_agent = Column(String, nullable=True)

    api_cert_expired_date = Column(DateTime, nullable=True)
    ca_cert_expired_date = Column(DateTime, nullable=True)
    etcd_cert_expired_date = Column(DateTime, nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class Database(Base, BaseMixin):
    __tablename__ = 'databases'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    db_type = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    status = Column(String, nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class License(Base, BaseMixin):
    __tablename__ = 'licenses'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    vendor = Column(String, nullable=True)
    license_type = Column(String, nullable=True)
    status = Column(String, nullable=True)
    instance_name = Column(String, nullable=True)
    comment = Column(String(length=3000), nullable=True)
    installed_at = Column(String, nullable=True)

    occurred_at = Column(DateTime, default=datetime.now)
    resolved_at = Column(DateTime, default=None)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class Vulnerability(Base, BaseMixin):
    __tablename__ = 'securities'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    progress = Column(String, nullable=True)
    status = Column(String, nullable=True)

    title = Column(String, nullable=True)
    task_type = Column(String, nullable=True)
    ticket_no = Column(String, nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


class PreventiveMaintenance(Base, BaseMixin):
    __tablename__ = 'regularchecks'

    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    region = Column(String, nullable=False)
    az = Column(Integer, nullable=False)
    tenant = Column(String, nullable=False)

    progress = Column(String, nullable=True)
    status = Column(String, nullable=True)

    freq = Column(String, nullable=True)
    vendor = Column(String, nullable=True)

    title = Column(String, nullable=True)
    description = Column(String(length=3000), nullable=True)

    creator = Column(String, nullable=True)
    reviewer = Column(String, nullable=True)
    updater = Column(String, nullable=True)


# class Report(Base, BaseMixin):
#     __tablename__ = 'reports'

#     year = Column(Integer, nullable=False)
#     month = Column(Integer, nullable=False)
#     region = Column(String, nullable=False)
#     az = Column(Integer, nullable=False)
#     tenant = Column(String, nullable=False)

#     progress = Column(String, nullable=True)
#     status = Column(String, nullable=True)

#     vendor = Column(String, nullable=True)
#     report_name = Column(String, nullable=True)
#     comment = Column(String(length=3000), nullable=True)

#     creator = Column(String, nullable=True)
#     reviewer = Column(String, nullable=True)
#     updater = Column(String, nullable=True)

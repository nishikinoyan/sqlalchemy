from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import hashlib

Base = declarative_base()

class User_test(Base):
    __tablename__ = 'User_test'
    user_id = Column(String(30),primary_key=True)
    user_password = Column(String(50))


def add_user(user_id,user_password):
    user_to_add = User_test(user_id=user_id,user_password=user_password)
    session = DBsession()
    session.add(user_to_add)
    session.commit()
    print('提交')
    session.close()

def delete_user(delete_user_id,delete_user_password):
    session = DBsession()
    session.query(User_test).filter_by(user_id = delete_user_id,user_password = delete_user_password).delete()
    session.commit()
    print('删除')
    session.close()

def query_user(query_user_id,query_user_password):
    session = DBsession()
    if(query_user_check(query_user_id,query_user_password) == True):
        user_result = session.query(User_test).filter_by(user_id=query_user_id,user_password=query_user_password).first()
        print('查询')
        print(user_result.user_id)
        print(user_result.user_password)
    else:
        print('没有这个用户')

def query_user_check(query_user_id,query_user_password):
    session = DBsession()
    user_result = session.query(User_test).filter_by(user_id=query_user_id,user_password=query_user_password).all()
    if(len(user_result) == 0):
        return False
    else:
        return True

def update_user(update_user_id,update_user_password,update_after_user_password):
    session = DBsession()
    session.query(User_test).filter_by(user_id = update_user_id,user_password = update_user_password).update({'user_password':update_after_user_password})
    print('更新')
    session.commit()
    session.close()


if __name__ == '__main__':
    engine_sql = create_engine('mysql+pymysql://flask:chen89726@47.74.240.209:3306/flask_login_test')
    DBsession = sessionmaker(bind=engine_sql)
    Base.metadata.create_all(engine_sql)


    while 1:
        print('请选操作：1:增加用户 2:删除用户  3:打印用户  4:改密码')
        choose = input()
        if(choose == '1'):
            print('输入用户名')
            add_user_id = input()
            print('输入用户密码')
            add_user_password = input()
            add_password_md5 = hashlib.new('md5')
            add_password_md5.update(bytes(add_user_password.encode('utf-8')))
            add_user(add_user_id,add_password_md5.hexdigest())

        if(choose == '2'):
            print('输入用户名')
            delete_user_id = input()
            print('输入用户密码')
            delete_user_password = input()
            delete_password_md5 = hashlib.new('md5')
            delete_password_md5.update(bytes(delete_user_password.encode('utf-8')))
            if(query_user_check(delete_user_id,delete_password_md5.hexdigest()) == True):
                delete_user(delete_user_id,delete_password_md5.hexdigest())
            else:
                print('密码错误')

        if(choose == '3'):
            print('输入用户名')
            query_user_id = input()
            print('输入用户密码')
            query_user_password = input()
            query_password_md5 = hashlib.new('md5')
            query_password_md5.update(bytes(query_user_password.encode('utf-8')))
            query_user(query_user_id,query_password_md5.hexdigest())

        if(choose == '4'):
            print('输入用户名')
            update_user_id = input()
            print('输入用户密码')
            update_user_password = input()
            update_password_md5 = hashlib.new('md5')
            update_password_md5.update(bytes(update_user_password.encode('utf-8')))

            if(query_user_check(update_user_id,update_password_md5.hexdigest()) == True):
                print('输入新密码')
                new_password = input()
                update_after_password_md5 = hashlib.new('md5')
                update_after_password_md5.update(bytes(new_password.encode('utf-8')))
                update_user(update_user_id,update_password_md5.hexdigest(),update_after_password_md5.hexdigest())
                print('修改成功')
            else:
                print('密码错误')



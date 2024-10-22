import pytest
from app import app, db
from server.models import Customer, Item, Review

@pytest.fixture(scope='function', autouse=True)
def clean_database():
    '''Ensure the database is clean before each test.'''
    with app.app_context():
        db.drop_all()  # Drop all tables
        db.create_all()  # Recreate all tables
        yield
        db.session.remove()  # Ensure session is cleaned up after each test

class TestAssociationProxy:
    '''Test association proxy for Customer model.'''

    def test_has_association_proxy(self):
        '''Ensure that Customer has association proxy to items.'''
        with app.app_context():
            c = Customer(name='Phil')
            i = Item(name='Insulated Mug', price=9.99)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            assert hasattr(c, 'items')
            assert i in c.items  # Check if the item is accessible through association proxy


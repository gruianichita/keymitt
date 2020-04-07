import datetime
from io import BytesIO
from unittest import TestCase

from app import app, mongo


class TestViews(TestCase):

    def test_upload(self):
        version = 7.3
        file_data = b"abcdef"
        file_name = 'test.py'
        data = {'version': version, 'file': (BytesIO(file_data), file_name)}

        response = app.test_client().post(
            "/application/", data=data, follow_redirects=True, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {'err_msg': ''})
        document = mongo.db.application.find_one({'version': version})
        self.assertIsNotNone(document)
        self.assertEqual(document.get('filebody'), file_data)
        self.assertEqual(document.get('filename'), file_name)

        data.pop('file')
        response = app.test_client().post(
            "/application/", data=data, follow_redirects=True, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

        mongo.db.application.delete_one({'filename': file_name})

    def test_download(self):
        version = 9.1
        file_data = b"testfile"
        file_name = 'test2.py'
        uri = '/application/'
        response = app.test_client().get(uri)

        self.assertEqual(response.status_code, 400)

        response = app.test_client().get(f'{uri}?version={version}')
        self.assertEqual(response.status_code, 400)

        now = datetime.datetime.now()
        app_data = {
            'updated_at': now,
            'filename': file_name,
            'filebody': file_data
        }

        mongo.db.application.update_one({'version': 10.1}, {'$set': app_data}, True)

        response = app.test_client().get(f'{uri}?version={version}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, file_data)

        mongo.db.application.delete_one({'filename': file_name})

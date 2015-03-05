import unittest
import difflib
from parsing import JavaParser
from repository import *


class TestJavaParser(unittest.TestCase):
    def setUp(self):
        self.code = """
            package org.feup.meoarenacustomer.app;
            import android.app.DownloadManager;

            import com.loopj.android.http.*;


            public class API {
                public String getUrl() {
                    return url;
                }

                public void setUrl(String url) {
                    this.url = url;
                }

                private String url;
                private final String PRODUCTION_URL = "http://neo.andrefreitas.pt:8081/api";
                private static AsyncHttpClient client = new AsyncHttpClient();

                public API(String url ){
                    this.url = url;
                }

                public API(){
                    this.url = PRODUCTION_URL;
                }


                public void login(String email, String password, AsyncHttpResponseHandler responseHandler){
                    RequestParams params = new RequestParams();
                    params.put("email", email);
                    params.put("password", password);
                    client.post(url + "/login", params, responseHandler);
                }

                public void register(String name, String email, String nif, String password, String ccNumber, String ccType, String ccValidity, AsyncHttpResponseHandler responseHandler){
                    RequestParams params = new RequestParams();
                    params.put("name", name);
                    params.put("email", email);
                    params.put("password", password);
                    params.put("nif", nif);
                    params.put("ccNumber", ccNumber);
                    params.put("ccType", ccType);
                    params.put("ccValidity", ccValidity);
                    client.post(url + "/customers", params, responseHandler);
                }

                public void getShows(AsyncHttpResponseHandler responseHandler) {
                    client.get(url + "/shows", responseHandler);
                }

            }"""

    def test_parse(self):
        """
        JavaParser.parse() should parse a class and methods from source code with their line numbers range
        """
        components = JavaParser.parse(self.code)
        self.assertTrue([[9, 11], ['API', 'getUrl']] in components)
        self.assertTrue([[13, 15], ['API', 'setUrl']] in components)
        self.assertTrue([[21, 23], ['API', 'API']] in components)
        self.assertTrue([[25, 27], ['API', 'API']] in components)
        self.assertTrue([[30, 35], ['API', 'login']] in components)
        self.assertTrue([[37, 47], ['API', 'register']] in components)
        self.assertTrue([[49, 51], ['API', 'getShows']] in components)

    def test_diff_case_a(self):
        """
        JavaParser.diff() should detect added, removed and modified methods
        """
        code_b = """
            package org.feup.meoarenacustomer.app;
            import android.app.DownloadManager;

            import com.loopj.android.http.*;


            public class API {
                public String getUrl() {
                    return url;
                }

                public void setUrl(String url) {
                    this.url = url;
                }

                private String url;
                private final String PRODUCTION_URL = "http://neo.andrefreitas.pt:8081/api";
                private static AsyncHttpClient client = new AsyncHttpClient();

                public API(String url ){
                    this.url = url;
                }

                public API(){
                    this.url = PRODUCTION_URL;
                }

                // Modified method
                public void login(String email, String password, AsyncHttpResponseHandler responseHandler){
                    RequestParams params = new RequestParams();
                    params.put("email", email);
                    client.post(url + "/login", params, responseHandler);
                }

                // Removed method register()

                // Added method
                public void recover(String name){
                    RequestParams params = new RequestParams();
                    params.put("name", name);
                    params.put("email", email);
                }

                // Added method
                public void outputShows(AsyncHttpResponseHandler responseHandler) {
                    client.get(url + "/shows", responseHandler);
                }

                public void getShows(AsyncHttpResponseHandler responseHandler) {
                    client.get(url + "/shows", responseHandler);
                }

            }"""

        diffs = JavaParser.diff(("API.java", self.code), ("API.java", code_b))
        self.assertTrue(DiffClass("API.java", class_a="API", class_b="API", modified=True) in diffs,
                        msg="It should recognize classes")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_a="login", method_b="login", modified=True)
                        in diffs, msg="It should recognize modified methods")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_a="register", removed=True) in diffs,
                        msg="It should recognize removed methods")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_b="recover", added=True) in diffs,
                        msg="It should recognize added methods")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_b="outputShows", added=True) in diffs,
                        msg="It should recognize added methods")
        self.assertEqual(len(diffs), 6)


if __name__ == '__main__':
    unittest.main()
# Copyright (c) 2015 Faculty of Engineering of the University of Porto
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Module with the Unit tests for the Java Parser. """

import unittest
from schwa.parsing import JavaParser
from schwa.repository import *


class TestJavaParser(unittest.TestCase):
    def setUp(self):
        self.code = """
            package org.feup.meoarenacustomer.app;
            import android.app.DownloadManager;

            import com.loopj.android.http.*;


            static class API {
                static String getUrl() {
                    return url;
                }

                static void setUrl(String url) {
                    this.url = url;
                }

                private String url;
                private final String PRODUCTION_URL = "http://neo.andrefreitas.pt:8081/api";
                private static AsyncHttpClient client = new AsyncHttpClient();

                static API(String url ){
                    this.url = url;
                }

                static API(){
                    this.url = PRODUCTION_URL;
                }


                static void login(String email, String password, AsyncHttpResponseHandler responseHandler){
                    RequestParams params = new RequestParams();
                    params.put("email", email);
                    params.put("password", password);
                    client.post(url + "/login", params, responseHandler);
                }

                static void register(String name, String email, String nif, String password, String ccNumber, String ccType, String ccValidity, AsyncHttpResponseHandler responseHandler){
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

                static void getShows(AsyncHttpResponseHandler responseHandler) {
                    client.get(url + "/shows", responseHandler);
                }

            }

             private class SOAPAPI{
                private void login(String name){
                    params.put("email", email);
                }
            }"""

    def test_parse(self):
        components = JavaParser.parse(self.code).classes

        classes_repr = [repr(c) for c in components]
        self.assertTrue('API<8,53>' in classes_repr)
        self.assertTrue('SOAPAPI<55,59>' in classes_repr)

        methods_repr = [repr(m) for m in components[0].methods]
        self.assertTrue('getUrl<9,11>' in methods_repr)
        self.assertTrue('API<21,23>' in methods_repr)
        self.assertTrue('API<25,27>' in methods_repr)
        self.assertTrue('login<30,35>' in methods_repr)
        self.assertTrue('register<37,47>' in methods_repr)
        self.assertTrue('getShows<49,51>' in methods_repr)

        methods_repr = [repr(m) for m in components[1].methods]
        self.assertTrue('login<56,58>' in methods_repr)

    def test_parse_with_anonymous_classes(self):
        code = """import javafx.event.ActionEvent;
                import javafx.event.EventHandler;
                import javafx.scene.Scene;
                import javafx.scene.control.Button;
                import javafx.scene.layout.StackPane;
                import javafx.stage.Stage;

                public class HelloWorld extends Application {
                    public static void main(String[] args) {
                        launch(args);
                    }

                    @Override
                    public void start(Stage primaryStage) {
                        primaryStage.setTitle("Hello World!");
                        Button btn = new Button();
                        btn.setText("Say 'Hello World'");
                        btn.setOnAction(new EventHandler<ActionEvent>() {

                            @Override
                            public void handle(ActionEvent event) {
                                System.out.println("Hello World!");
                            }
                        });

                        StackPane root = new StackPane();
                        root.getChildren().add(btn);
                        primaryStage.setScene(new Scene(root, 300, 250));
                        primaryStage.show();
                    }
                }"""
        components = JavaParser.parse(code).classes
        classes_repr = [repr(c) for c in components]
        self.assertTrue('HelloWorld<8,31>' in classes_repr)
        methods_repr = [repr(m) for m in components[0].methods]
        self.assertTrue('main<9,11>' in methods_repr)
        self.assertTrue('start<14,30>' in methods_repr)

    def test_parse_nested_classes(self):
        code = """public class ShadowTest {

            public int x = 0;

            class FirstLevel {

                public int x = 1;

                void methodInFirstLevel(int x) {
                    System.out.println("x = " + x);
                    System.out.println("this.x = " + this.x);
                    System.out.println("ShadowTest.this.x = " + ShadowTest.this.x);
                }
            }

            public static void main(String... args) {
                ShadowTest st = new ShadowTest();
                ShadowTest.FirstLevel fl = st.new FirstLevel();
                fl.methodInFirstLevel(23);
            }
        }"""

        components = JavaParser.parse(code).classes

        classes_repr = [repr(c) for c in components]
        self.assertTrue('ShadowTest<1,21>' in classes_repr)
        self.assertEqual(len(classes_repr), 1)
        methods_repr = [repr(m) for m in components[0].methods]
        self.assertTrue('main<16,20>' in methods_repr)
        self.assertEqual(len(methods_repr), 1)

        classes_repr = [repr(c) for c in components[0].classes]
        self.assertTrue('FirstLevel<5,14>' in classes_repr)
        self.assertEqual(len(classes_repr), 1)
        methods_repr = [repr(m) for m in components[0].classes[0].methods]
        self.assertTrue('methodInFirstLevel<9,13>' in methods_repr)
        self.assertEqual(len(methods_repr), 1)

    def test_compressed_code(self):
        code = """public class ShadowTest{public int x=0;class FirstLevel{public int x=1;void methodInFirstLevel""" \
            + """(int x){System.out.println("x = "+x);System.out.println("this.x = "+this.x);""" \
            + """System.out.println("ShadowTest.this.x = "+ShadowTest.this.x);}}public static void main(String...""" \
            + """args){ShadowTest st=new ShadowTest();ShadowTest.FirstLevel fl=st.new FirstLevel();""" \
            + "fl.methodInFirstLevel(23);}}"""
        components = JavaParser.parse(code).classes

        classes_repr = [repr(c) for c in components]
        self.assertTrue('ShadowTest<1,1>' in classes_repr)
        methods_repr = [repr(m) for m in components[0].methods]
        self.assertTrue('main<1,1>' in methods_repr)

        classes_repr = [repr(c) for c in components[0].classes]
        self.assertTrue('FirstLevel<1,1>' in classes_repr)
        methods_repr = [repr(m) for m in components[0].classes[0].methods]
        self.assertTrue('methodInFirstLevel<1,1>' in methods_repr)

    def test_abstract_class(self):
        code = """public abstract class GraphicObject {
           // declare fields
           // declare nonabstract methods
           abstract void draw();
        }"""
        components = JavaParser.parse(code).classes
        classes_repr = [repr(c) for c in components]
        self.assertTrue('GraphicObject<1,5>' in classes_repr)
        methods_repr = [repr(m) for m in components[0].methods]
        self.assertTrue('draw<4,4>' in methods_repr)

    def test_empty_methods(self):
        code = """private class SOAPAPI{
                private void login(String name)
                {

                }
                private void login2(String name){

                }}"""

        components = JavaParser.parse(code).classes
        classes_repr = [repr(c) for c in components]
        self.assertTrue('SOAPAPI<1,8>' in classes_repr)
        methods_repr = [repr(m) for m in components[0].methods]
        self.assertTrue('login<2,5>' in methods_repr)
        self.assertTrue('login2<6,8>' in methods_repr)

    def test_diff_case_a(self):
        code_b = """
            package org.feup.meoarenacustomer.app;
            import android.app.DownloadManager;

            import com.loopj.android.http.*;


            static class API {
                static String getUrl() {
                    return url;
                }

                static void setUrl(String url) {
                    this.url = url;
                }

                private String url;
                private final String PRODUCTION_URL = "http://neo.andrefreitas.pt:8081/api";
                private static AsyncHttpClient client = new AsyncHttpClient();

                static API(String url ){
                    this.url = url;
                }

                static API(){
                    this.url = PRODUCTION_URL;
                }

                // Modified method
                static void login(String email, String password, AsyncHttpResponseHandler responseHandler){
                    RequestParams params = new RequestParams();
                    params.put("email", email);
                    client.post(url + "/login", params, responseHandler);
                }

                // Removed method register()

                // Added method
                static void recover(String name){
                    RequestParams params = new RequestParams();
                    params.put("name", name);
                    params.put("email", email);
                }

                // Added method
                static void outputShows(AsyncHttpResponseHandler responseHandler) {
                    client.get(url + "/shows", responseHandler);
                }

                static void getShows(AsyncHttpResponseHandler responseHandler) {
                    client.get(url + "/shows", responseHandler);
                }

            }

            private class JSONAPI{
                private void recover(String name){
                    RequestParams params = new RequestParams();
                    params.put("name", name);
                    params.put("email", email);
                }
            }
            """

        diffs = JavaParser.diff(("API.java", self.code), ("API.java", code_b))

        # TODO: Test nested classes

        self.assertTrue(DiffClass("API.java", class_a="API", class_b="API", modified=True) in diffs,
                        msg="It should recognize modified classes")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_a="login", method_b="login", modified=True)
                        in diffs, msg="It should recognize modified methods")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_a="register", removed=True) in diffs,
                        msg="It should recognize removed methods")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_b="recover", added=True) in diffs,
                        msg="It should recognize added methods")
        self.assertTrue(DiffMethod("API.java", class_name="API", method_b="outputShows", added=True) in diffs,
                        msg="It should recognize added methods")
        self.assertTrue(DiffClass("API.java", class_a="SOAPAPI", removed=True) in diffs,
                        msg="It should recognize removed classes")
        self.assertTrue(DiffClass("API.java", class_b="JSONAPI", added=True) in diffs,
                        msg="It should recognize added classes")
        self.assertTrue(DiffMethod("API.java", class_name="SOAPAPI", method_a="login", removed=True) in diffs,
                        msg="It should recognize removed methods")
        self.assertTrue(DiffMethod("API.java", class_name="JSONAPI", method_b="recover", added=True) in diffs,
                        msg="It should recognize added methods")

        self.assertEqual(len(diffs), 9)


if __name__ == '__main__':
    unittest.main()
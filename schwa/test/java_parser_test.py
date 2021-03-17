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

    def set_to_str(self, set):
        return [str(x) for x in set]

    def test_parse(self):
        file = JavaParser.parse(Granularity.LINE, "dummy.java", self.code)
        # Classes
        classes = sorted(file.get_classes())
        clazz_a = classes[0]
        self.assertEquals('API<8,53>', str(clazz_a))
        clazz_b = classes[1]
        self.assertEquals('SOAPAPI<55,59>', str(clazz_b))
        # Methods of API
        clazz_a_methods = self.set_to_str(clazz_a.get_methods())
        self.assertEquals(7, len(clazz_a_methods))
        self.assertTrue('getUrl()<9,11>' in clazz_a_methods)
        self.assertTrue('setUrl(String)<13,15>' in clazz_a_methods)
        self.assertTrue('API(String)<21,23>' in clazz_a_methods)
        self.assertTrue('API()<25,27>' in clazz_a_methods)
        self.assertTrue('login(String,String,AsyncHttpResponseHandler)<30,35>' in clazz_a_methods)
        self.assertTrue('register(String,String,String,String,String,String,String,AsyncHttpResponseHandler)<37,47>' in clazz_a_methods)
        self.assertTrue('getShows(AsyncHttpResponseHandler)<49,51>' in clazz_a_methods)
        # Methods of SOAPAPI
        clazz_b_methods = self.set_to_str(clazz_b.get_methods())
        self.assertEquals(1, len(clazz_b_methods))
        self.assertTrue('login(String)<56,58>' in clazz_b_methods)

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
        file = JavaParser.parse(Granularity.LINE, "dummy.java", code)
        # Class
        clazz = list(file.get_classes())[0]
        self.assertEquals('HelloWorld<8,31>', str(clazz))
        # Methods
        clazz_methods = list(sorted(clazz.get_methods()))
        self.assertEquals(2, len(clazz_methods))
        self.assertEquals('main(String)<9,11>', str(clazz_methods[0]))
        self.assertEquals('start(Stage)<14,30>', str(clazz_methods[1]))
        # Methods of methods
        method_methods = list(clazz_methods[1].get_methods())
        self.assertEquals(1, len(method_methods))
        self.assertEquals('handle(ActionEvent)<21,23>', str(method_methods[0]))

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

        file = JavaParser.parse(Granularity.LINE, "dummy.java", code)
        # Classes
        classes = sorted(file.get_classes())
        clazz_a = classes[0]
        clazz_b = classes[1]
        self.assertEquals('ShadowTest<1,21>', str(clazz_a))
        self.assertEquals('FirstLevel<5,14>', str(clazz_b))
        # Methods
        clazz_a_methods = self.set_to_str(clazz_a.get_methods())
        self.assertEquals(1, len(clazz_a_methods))
        self.assertTrue('main(String)<16,20>' in clazz_a_methods)
        clazz_b_methods = self.set_to_str(clazz_b.get_methods())
        self.assertEquals(1, len(clazz_b_methods))
        self.assertTrue('methodInFirstLevel(int)<9,13>' in clazz_b_methods)

    def test_compressed_code(self):
        code = """public class ShadowTest{public int x=0;class FirstLevel{public int x=1;void methodInFirstLevel""" \
            + """(int x){System.out.println("x = "+x);System.out.println("this.x = "+this.x);""" \
            + """System.out.println("ShadowTest.this.x = "+ShadowTest.this.x);}}public static void main(String...""" \
            + """args){ShadowTest st=new ShadowTest();ShadowTest.FirstLevel fl=st.new FirstLevel();""" \
            + "fl.methodInFirstLevel(23);}}"""
        file = JavaParser.parse(Granularity.LINE, "dummy.java", code)
        # Classes
        classes = sorted(file.get_classes())
        clazz_a = classes[0]
        clazz_b = classes[1]
        self.assertEquals('ShadowTest<1,1>', str(clazz_a))
        self.assertEquals('FirstLevel<1,1>', str(clazz_b))
        # Methods
        clazz_a_methods = self.set_to_str(clazz_a.get_methods())
        self.assertEquals(1, len(clazz_a_methods))
        self.assertTrue('main(String)<1,1>' in clazz_a_methods)
        clazz_b_methods = self.set_to_str(clazz_b.get_methods())
        self.assertEquals(1, len(clazz_b_methods))
        self.assertTrue('methodInFirstLevel(int)<1,1>' in clazz_b_methods)

    def test_abstract_class(self):
        code = """public abstract class GraphicObject {
           // declare fields
           // declare nonabstract methods
           abstract void draw();
        }"""
        file = JavaParser.parse(Granularity.LINE, "dummy.java", code)
        # Class
        clazz = list(file.get_classes())[0]
        self.assertEquals('GraphicObject<1,5>', str(clazz))
        # Method
        clazz_methods = self.set_to_str(clazz.get_methods())
        self.assertEquals(1, len(clazz_methods))
        self.assertTrue('draw()<4,4>' in clazz_methods)

    def test_empty_methods(self):
        code = """private class SOAPAPI{
                private void login(String name)
                {

                }
                private void login2(String name){

                }}"""

        file = JavaParser.parse(Granularity.LINE, "dummy.java", code)
        # Class
        clazz = list(file.get_classes())[0]
        self.assertEquals('SOAPAPI<1,8>', str(clazz))
        # Methods
        clazz_methods = self.set_to_str(clazz.get_methods())
        self.assertEquals(2, len(clazz_methods))
        self.assertTrue('login(String)<2,5>' in clazz_methods)
        self.assertTrue('login2(String)<6,8>' in clazz_methods)

    def test_methods_with_same_name_but_different_signature(self):
        code = """public class Foo {
            public void bar() {
                // NO-OP
            }
            public void bar(int i) {
                // NO-OP
            }
            public void bar(java.util.List<?> l) {
                // NO-OP
            }
            public void bar(java.util.ArrayList<Integer> a) {
                // NO-OP
            }
        }
        """

        file = JavaParser.parse(Granularity.LINE, "dummy.java", code)
        # Class
        clazz = list(file.get_classes())[0]
        self.assertEquals('Foo<1,14>', str(clazz))
        # Methods
        clazz_methods = self.set_to_str(clazz.get_methods())
        self.assertEquals(4, len(clazz_methods))
        self.assertTrue('bar()<2,4>' in clazz_methods)
        self.assertTrue('bar(int)<5,7>' in clazz_methods)
        self.assertTrue('bar(java.util.List)<8,10>' in clazz_methods)
        self.assertTrue('bar(java.util.ArrayList)<11,13>' in clazz_methods)

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

        diffs = sorted(JavaParser.diff(Granularity.METHOD, ("API.java", self.code), ("API.java", code_b)))
        self.assertEqual(9, len(diffs))

        # added class None,JSONAPI<56,62> in API.java<2,62>
        added_class = diffs[0]
        self.assertFalse(added_class.renamed)
        self.assertFalse(added_class.modified)
        self.assertTrue(added_class.added)
        self.assertFalse(added_class.removed)
        self.assertEquals(None, added_class.version_a)
        self.assertEquals('JSONAPI<56,62>', str(added_class.version_b))
        self.assertEquals('API.java<2,62>', str(added_class.version_b.parent))

        # added method None,outputShows(AsyncHttpResponseHandler)<46,48> in API<8,54>
        added_method = diffs[1]
        self.assertFalse(added_method.renamed)
        self.assertFalse(added_method.modified)
        self.assertTrue(added_method.added)
        self.assertFalse(added_method.removed)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('outputShows(AsyncHttpResponseHandler)<46,48>', str(added_method.version_b))
        self.assertEquals('API<8,54>', str(added_method.version_b.parent))

        # added method None,recover(String)<39,43> in API<8,54>
        added_method = diffs[2]
        self.assertFalse(added_method.renamed)
        self.assertFalse(added_method.modified)
        self.assertTrue(added_method.added)
        self.assertFalse(added_method.removed)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('recover(String)<39,43>', str(added_method.version_b))
        self.assertEquals('API<8,54>', str(added_method.version_b.parent))

        # added method None,recover(String)<57,61> in JSONAPI<56,62>
        added_method = diffs[3]
        self.assertFalse(added_method.renamed)
        self.assertFalse(added_method.modified)
        self.assertTrue(added_method.added)
        self.assertFalse(added_method.removed)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('recover(String)<57,61>', str(added_method.version_b))
        self.assertEquals('JSONAPI<56,62>', str(added_method.version_b.parent))

        # modified class API<8,53>,API<8,54> in API.java<2,62>
        modified_class = diffs[4]
        self.assertFalse(modified_class.renamed)
        self.assertTrue(modified_class.modified)
        self.assertFalse(modified_class.added)
        self.assertFalse(modified_class.removed)
        self.assertEquals('API<8,53>', str(modified_class.version_a))
        self.assertEquals('API<8,54>', str(modified_class.version_b))
        self.assertEquals('API.java<2,62>', str(modified_class.version_b.parent))

        # modified method login(String,String,AsyncHttpResponseHandler)<30,35>,login(String,String,AsyncHttpResponseHandler)<30,34> in API<8,54>
        modified_method = diffs[5]
        self.assertFalse(modified_method.renamed)
        self.assertTrue(modified_method.modified)
        self.assertFalse(modified_method.added)
        self.assertFalse(modified_method.removed)
        self.assertEquals('login(String,String,AsyncHttpResponseHandler)<30,35>', str(modified_method.version_a))
        self.assertEquals('login(String,String,AsyncHttpResponseHandler)<30,34>', str(modified_method.version_b))
        self.assertEquals('API<8,54>', str(modified_method.version_b.parent))

        # removed class SOAPAPI<55,59>,None in API.java<2,59>
        removed_class = diffs[6]
        self.assertFalse(removed_class.renamed)
        self.assertFalse(removed_class.modified)
        self.assertFalse(removed_class.added)
        self.assertTrue(removed_class.removed)
        self.assertEquals('SOAPAPI<55,59>', str(removed_class.version_a))
        self.assertEquals(None, removed_class.version_b)
        self.assertEquals('API.java<2,59>', str(removed_class.version_a.parent))

        # removed method login(String)<56,58>,None in SOAPAPI<55,59>
        removed_method = diffs[7]
        self.assertFalse(removed_method.renamed)
        self.assertFalse(removed_method.modified)
        self.assertFalse(removed_method.added)
        self.assertTrue(removed_method.removed)
        self.assertEquals('login(String)<56,58>', str(removed_method.version_a))
        self.assertEquals(None, removed_method.version_b)
        self.assertEquals('SOAPAPI<55,59>', str(removed_method.version_a.parent))

        # removed method register(String,String,String,String,String,String,String,AsyncHttpResponseHandler)<37,47>,None in API<8,53>
        removed_method = diffs[8]
        self.assertFalse(removed_method.renamed)
        self.assertFalse(removed_method.modified)
        self.assertFalse(removed_method.added)
        self.assertTrue(removed_method.removed)
        self.assertEquals('register(String,String,String,String,String,String,String,AsyncHttpResponseHandler)<37,47>', str(removed_method.version_a))
        self.assertEquals(None, removed_method.version_b)
        self.assertEquals('API<8,53>', str(removed_method.version_a.parent))

if __name__ == '__main__':
    unittest.main()
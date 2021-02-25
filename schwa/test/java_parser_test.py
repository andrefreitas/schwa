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

    def is_in(self, file, klass=None, method=None, line=None):

        if klass != None and method == None:
            classes_repr = [str(c) for c in file.get_classes()]
            print(str(klass))
            print(str(classes_repr))
            self.assertTrue(klass in classes_repr)
            return
        elif klass != None and method != None:
            for c in file.get_classes():
                if str(c) == klass:
                    methods_repr = [str(m) for m in c.get_methods()]
                    print(str(method))
                    print(str(methods_repr))
                    self.assertTrue(method in methods_repr)
                    return
        elif klass != None and method != None and line != None:
            for c in file.get_classes():
                if str(c) == klass:
                    for m in c.get_methods():
                        if str(m) == method:
                            lines_repr = [str(l) for l in m.get_lines()]
                            print(str(l))
                            print(str(lines_repr))
                            self.assertTrue(line in lines_repr)
                            return

        self.fail("No condition has been met")

    def test_parse(self):
        file = JavaParser.parse(Granularity.LINE, "dummy.java", self.code)
        # Classes
        self.is_in(file=file, klass='API<8,53>')
        self.is_in(file=file, klass='SOAPAPI<55,59>')
        # Methods of API
        self.is_in(file=file, klass='API<8,53>', method='getUrl()<9,11>')
        self.is_in(file=file, klass='API<8,53>', method='API(String)<21,23>')
        self.is_in(file=file, klass='API<8,53>', method='API()<25,27>')
        self.is_in(file=file, klass='API<8,53>', method='login(String,String,AsyncHttpResponseHandler)<30,35>')
        self.is_in(file=file, klass='API<8,53>', method='register(String,String,String,String,String,String,String,AsyncHttpResponseHandler)<37,47>')
        self.is_in(file=file, klass='API<8,53>', method='getShows(AsyncHttpResponseHandler)<49,51>')
        # Methods of SOAPAPI
        self.is_in(file=file, klass='SOAPAPI<55,59>', method='login(String)<56,58>')

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
        self.is_in(file=file, klass='HelloWorld<8,31>')
        # Methods
        self.is_in(file=file, klass='HelloWorld<8,31>', method='main(String)<9,11>')
        self.is_in(file=file, klass='HelloWorld<8,31>', method='start(Stage)<14,30>')
        self.is_in(file=file, klass='HelloWorld<8,31>', method='handle(ActionEvent)<21,23>')

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
        self.is_in(file=file, klass='ShadowTest<1,21>')
        self.is_in(file=file, klass='FirstLevel<5,14>')
        # Methods
        self.is_in(file=file, klass='ShadowTest<1,21>', method='main(String)<16,20>')
        self.is_in(file=file, klass='FirstLevel<5,14>', method='methodInFirstLevel(int)<9,13>')

    def test_compressed_code(self):
        code = """public class ShadowTest{public int x=0;class FirstLevel{public int x=1;void methodInFirstLevel""" \
            + """(int x){System.out.println("x = "+x);System.out.println("this.x = "+this.x);""" \
            + """System.out.println("ShadowTest.this.x = "+ShadowTest.this.x);}}public static void main(String...""" \
            + """args){ShadowTest st=new ShadowTest();ShadowTest.FirstLevel fl=st.new FirstLevel();""" \
            + "fl.methodInFirstLevel(23);}}"""
        file = JavaParser.parse(Granularity.LINE, "dummy.java", code)
        # Classes
        self.is_in(file=file, klass='ShadowTest<1,1>')
        self.is_in(file=file, klass='FirstLevel<1,1>')
        # Methods
        self.is_in(file=file, klass='ShadowTest<1,1>', method='main(String)<1,1>')
        self.is_in(file=file, klass='FirstLevel<1,1>', method='methodInFirstLevel(int)<1,1>')

    def test_abstract_class(self):
        code = """public abstract class GraphicObject {
           // declare fields
           // declare nonabstract methods
           abstract void draw();
        }"""
        file = JavaParser.parse(Granularity.LINE, "dummy.java", code)
        # Class
        self.is_in(file=file, klass='GraphicObject<1,5>')
        # Method
        self.is_in(file=file, klass='GraphicObject<1,5>', method='draw()<4,4>')

    def test_empty_methods(self):
        code = """private class SOAPAPI{
                private void login(String name)
                {

                }
                private void login2(String name){

                }}"""

        file = JavaParser.parse(Granularity.LINE, "dummy.java", code)
        # Class
        self.is_in(file=file, klass='SOAPAPI<1,8>')
        # Methods
        self.is_in(file=file, klass='SOAPAPI<1,8>', method='login(String)<2,5>')
        self.is_in(file=file, klass='SOAPAPI<1,8>', method='login2(String)<6,8>')

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
        self.is_in(file=file, klass='Foo<1,14>')
        # Methods
        self.is_in(file=file, klass='Foo<1,14>', method='bar()<2,4>')
        self.is_in(file=file, klass='Foo<1,14>', method='bar(int)<5,7>')
        self.is_in(file=file, klass='Foo<1,14>', method='bar(java.util.List)<8,10>')
        self.is_in(file=file, klass='Foo<1,14>', method='bar(java.util.ArrayList)<11,13>')

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

        diffs = JavaParser.diff(Granularity.METHOD, ("API.java", self.code), ("API.java", code_b))
        self.assertEqual(len(diffs), 9)

        print(diffs) # FIXME remove me
        print(str(len(diffs)))

        # TODO: Test nested classes

# added class None,JSONAPI<56,60> in API.java<1,9223372036854775807>
# removed class SOAPAPI<55,57>,None in API.java<1,9223372036854775807>
# modified class API<8,50>,API<8,50> in API.java<1,9223372036854775807>
# ---
# added method None,recover(String)<57,60> in JSONAPI<56,60>
# added method None,outputShows(AsyncHttpResponseHandler)<46,47> in API<8,51>
# added method None,recover(String)<39,42> in API<8,51>
# removed method login(String)<56,57>,None in SOAPAPI<55,57>
# removed method register(String,String,String,String,String,String,String,AsyncHttpResponseHandler)<37,46>,None in API<8,50>
# modified method login(String,String,AsyncHttpResponseHandler)<30,34>,login(String,String,AsyncHttpResponseHandler)<30,34> in API<8,50>

        self.assertTrue(DiffClass("API.java", class_a="API", class_b="API", modified=True) in diffs,
                        msg="It should recognize modified classes")
        # self.assertTrue(DiffMethod("API.java", class_name="API", method_a="login(String, String, AsyncHttpResponseHandler)", method_b="login(String, String, AsyncHttpResponseHandler)", modified=True)
        #                 in diffs, msg="It should recognize modified methods")
        # self.assertTrue(DiffMethod("API.java", class_name="API", method_a="register(String, String, String, String, String, String, String, AsyncHttpResponseHandler)", removed=True) in diffs,
        #                 msg="It should recognize removed methods")
        # self.assertTrue(DiffMethod("API.java", class_name="API", method_b="recover(String)", added=True) in diffs,
        #                 msg="It should recognize added methods")
        # self.assertTrue(DiffMethod("API.java", class_name="API", method_b="outputShows(AsyncHttpResponseHandler)", added=True) in diffs,
        #                 msg="It should recognize added methods")
        # self.assertTrue(DiffClass("API.java", class_a="SOAPAPI", removed=True) in diffs,
        #                 msg="It should recognize removed classes")
        # self.assertTrue(DiffClass("API.java", class_b="JSONAPI", added=True) in diffs,
        #                 msg="It should recognize added classes")
        # self.assertTrue(DiffMethod("API.java", class_name="SOAPAPI", method_a="login(String)", removed=True) in diffs,
        #                 msg="It should recognize removed methods")
        # self.assertTrue(DiffMethod("API.java", class_name="JSONAPI", method_b="recover(String)", added=True) in diffs,
        #                 msg="It should recognize added methods")


if __name__ == '__main__':
    unittest.main()
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
        """
        JavaParser.parse() should parse a class and methods from source code with their line numbers range
        """
        components = JavaParser.parse(self.code)
        self.assertTrue([9, 11, 'API', 'getUrl'] in components)
        self.assertTrue([13, 15, 'API', 'setUrl'] in components)
        self.assertTrue([21, 23, 'API', 'API'] in components)
        self.assertTrue([25, 27, 'API', 'API'] in components)
        self.assertTrue([30, 35, 'API', 'login'] in components)
        self.assertTrue([37, 47, 'API', 'register'] in components)
        self.assertTrue([49, 51, 'API', 'getShows'] in components)
        self.assertTrue([56, 58, 'SOAPAPI', 'login'] in components)

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
        components = JavaParser.parse(code)
        self.assertTrue([9, 11, 'HelloWorld', 'main'] in components)
        self.assertTrue([14, 30, 'HelloWorld', 'start'] in components)

    def test_parse_class_without_bracket(self):
        code = """/* CallingMethodsInSameClass.java
         *
         * illustrates how to call static methods a class
         * from a method in the same class
         */

        public class CallingMethodsInSameClass
        {
            public static void main(String[] args) {
                printOne();
                printOne();
                printTwo();
            }

            public static void printOne() {
                System.out.println("Hello World");
            }

            public static void printTwo() {
                printOne();
                printOne();
            }
        }"""
        components = JavaParser.parse(code)
        self.assertTrue([9, 13, 'CallingMethodsInSameClass', 'main'] in components)
        self.assertTrue([15, 17, 'CallingMethodsInSameClass', 'printOne'] in components)
        self.assertTrue([19, 22, 'CallingMethodsInSameClass', 'printTwo'] in components)

    def test_diff_case_a(self):
        """
        JavaParser.diff() should detect added, removed and modified methods
        """
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
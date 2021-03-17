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

""" Module with the Unit tests for the Git Extractor. """

import unittest
import tempfile
import os
import shutil
import time
import git
from schwa.extraction import GitExtractor
from schwa.repository import *


class TestGitExtractor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = os.path.join(tempfile.gettempdir(), "repo-test")
        if os.path.exists(self.temp_dir):
                 shutil.rmtree(self.temp_dir)
        self.repo = git.Repo.init(self.temp_dir)
        self.repo.git.execute(["git", "config", "user.email", "petergriffin@familyguy.com"])
        self.repo.git.execute(["git", "config", "user.name", "Peter Griffin"])

    def testExtraction(self):
        code = """
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

        """ First Commit """
        # Added API.java
        file_path = os.path.join(self.temp_dir, "API.java")
        f = open(file_path, "w")
        f.write(code)
        f.close()
        self.repo.git.add(file_path)
        # Added README.txt
        file_path = os.path.join(self.temp_dir, "README.txt")
        f = open(file_path, "w")
        f.write("TODO: Write readme")
        f.close()
        self.repo.git.add(file_path)
        self.repo.git.commit(m='First commit')
        creation_timestamp = time.time()

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

        """ Second commit """
        # Modified API.java
        file_path = os.path.join(self.temp_dir, "API.java")
        f = open(file_path, "w")
        f.write(code_b)
        f.close()
        self.repo.git.add(file_path)
        self.repo.git.commit(m='Second commit')

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

        """ Third commit """
        # Added CallingMethodsInSameClass.java
        file_path = os.path.join(self.temp_dir, "CallingMethodsInSameClass.java")
        f = open(file_path, "w")
        f.write(code)
        f.close()
        self.repo.git.add(file_path)
        # Modified README.txt
        file_path = os.path.join(self.temp_dir, "README.txt")
        f = open(file_path, "w")
        f.write("AUTHORS: Peter Griffin - peter@familyguy.com")
        f.close()
        self.repo.git.add(file_path)
        self.repo.git.commit(m='Third commit')

        """ Fourth Commit """
        # Deleted CallingMethodsInSameClass.java
        file_path = os.path.join(self.temp_dir, "CallingMethodsInSameClass.java")
        self.repo.git.rm(file_path)
        # Renamed API.java to API2.java
        file_path_a = os.path.join(self.temp_dir, "API.java")
        file_path_b = os.path.join(self.temp_dir, "API2.java")
        self.repo.git.mv(file_path_a, file_path_b)
        self.repo.git.commit(m='Fourth commit')

        """ Fifth Commit"""
        # Modified README.txt
        file_path = os.path.join(self.temp_dir, "README.txt")
        f = open(file_path, "w")
        f.write("AUTHORS: Peter Griffin and Louis Griffin")
        f.close()
        self.repo.git.add(file_path)
        self.repo.git.commit(m='Fifth commit')

        """ Sixth Commit"""
        # Added ShadowTest.java
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
        file_path = os.path.join(self.temp_dir, "ShadowTest.java")
        f = open(file_path, "w")
        f.write(code)
        f.close()
        self.repo.git.add(file_path)
        self.repo.git.commit(m='Sixth commit')

        """ Extract """
        extractor = GitExtractor(self.temp_dir)
        repository = extractor.extract(granularity=Granularity.METHOD, parallel=False)

        """ Tests """
        self.assertEqual(len(repository.commits), 5, msg="It should only extract commits related to code")
        self.assertTrue(repository.begin_ts < creation_timestamp, msg="It should extract the timestamp of first commit")

        ##
        # First commit
        self.assertEqual(repository.commits[0].message, "First commit\n")
        self.assertEqual(repository.commits[0].author, "petergriffin@familyguy.com")
        diffs = sorted(repository.commits[0].diffs)
        self.assertEqual(11, len(diffs))

        # added class None,API<8,53> in API.java<2,59>
        added_class = diffs[0]
        self.assertTrue(added_class.renamed == added_class.modified == added_class.removed == False)
        self.assertTrue(added_class.added)
        self.assertEquals(None, added_class.version_a)
        self.assertEquals('API', added_class.version_b.name)
        self.assertEquals('API.java', added_class.version_b.parent.name)

        # added class None,SOAPAPI<55,59> in API.java<2,59>
        added_class = diffs[1]
        self.assertTrue(added_class.renamed == added_class.modified == added_class.removed == False)
        self.assertTrue(added_class.added)
        self.assertEquals(None, added_class.version_a)
        self.assertEquals('SOAPAPI', added_class.version_b.name)
        self.assertEquals('API.java', added_class.version_b.parent.name)

        # added file None,API.java
        added_file = diffs[2]
        self.assertTrue(added_file.renamed == added_file.modified == added_file.removed == False)
        self.assertTrue(added_file.added)
        self.assertEquals(None, added_file.version_a)
        self.assertEquals('API.java', added_file.version_b.name)
        self.assertEquals(None, added_file.version_b.parent)

        # added method None,API()<25,27> in API<8,53>
        added_method = diffs[3]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('API()', added_method.version_b.name)
        self.assertEquals('API', added_method.version_b.parent.name)

        # added method None,API(String)<21,23> in API<8,53>
        added_method = diffs[4]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('API(String)', added_method.version_b.name)
        self.assertEquals('API', added_method.version_b.parent.name)

        # added method None,getShows(AsyncHttpResponseHandler)<49,51> in API<8,53>
        added_method = diffs[5]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('getShows(AsyncHttpResponseHandler)', added_method.version_b.name)
        self.assertEquals('API', added_method.version_b.parent.name)

        # added method None,getUrl()<9,11> in API<8,53>
        added_method = diffs[6]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('getUrl()', added_method.version_b.name)
        self.assertEquals('API', added_method.version_b.parent.name)

        # added method None,login(String)<56,58> in SOAPAPI<55,59>
        added_method = diffs[7]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('login(String)', added_method.version_b.name)
        self.assertEquals('SOAPAPI', added_method.version_b.parent.name)

        # added method None,login(String,String,AsyncHttpResponseHandler)<30,35> in API<8,53>
        added_method = diffs[8]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('login(String,String,AsyncHttpResponseHandler)', added_method.version_b.name)
        self.assertEquals('API', added_method.version_b.parent.name)

        # added method None,register(String,String,String,String,String,String,String,AsyncHttpResponseHandler)<37,47> in API<8,53>
        added_method = diffs[9]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('register(String,String,String,String,String,String,String,AsyncHttpResponseHandler)', added_method.version_b.name)
        self.assertEquals('API', added_method.version_b.parent.name)

        # added method None,setUrl(String)<13,15> in API<8,53>
        added_method = diffs[10]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('setUrl(String)', added_method.version_b.name)
        self.assertEquals('API', added_method.version_b.parent.name)

        ##
        # Second commit
        self.assertEqual(repository.commits[1].message, "Second commit\n")
        diffs = sorted(repository.commits[1].diffs)
        self.assertEqual(10, len(diffs))

        # added class None,JSONAPI<56,62> in API.java<2,62>
        added_class = diffs[0]
        self.assertTrue(added_class.renamed == added_class.modified == added_class.removed == False)
        self.assertTrue(added_class.added)
        self.assertEquals(None, added_class.version_a)
        self.assertEquals('JSONAPI', added_class.version_b.name)
        self.assertEquals('API.java', added_class.version_b.parent.name)

        # added method None,outputShows(AsyncHttpResponseHandler)<46,48> in API<8,54>
        added_method = diffs[1]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('outputShows(AsyncHttpResponseHandler)', added_method.version_b.name)
        self.assertEquals('API', added_method.version_b.parent.name)

        # added method None,recover(String)<39,43> in API<8,54>
        added_method = diffs[2]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('recover(String)', added_method.version_b.name)
        self.assertEquals('API', added_method.version_b.parent.name)

        # added method None,recover(String)<57,61> in JSONAPI<56,62>
        added_method = diffs[3]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('recover(String)', added_method.version_b.name)
        self.assertEquals('JSONAPI', added_method.version_b.parent.name)

        # modified class API<8,53>,API<8,54> in API.java<2,62>
        modified_class = diffs[4]
        self.assertTrue(modified_class.renamed == modified_class.added == modified_class.removed == False)
        self.assertTrue(modified_class.modified)
        self.assertEquals('API', modified_class.version_a.name)
        self.assertEquals('API', modified_class.version_b.name)
        self.assertEquals('API.java', modified_class.version_b.parent.name)

        # modified file API.java,API.java
        modified_file = diffs[5]
        self.assertTrue(modified_file.renamed == modified_file.added == modified_file.removed == False)
        self.assertTrue(modified_file.modified)
        self.assertEquals('API.java', modified_file.version_a.name)
        self.assertEquals('API.java', modified_file.version_b.name)
        self.assertEquals(None, modified_file.version_b.parent)

        # modified method login(String,String,AsyncHttpResponseHandler)<30,35>,login(String,String,AsyncHttpResponseHandler)<30,34> in API<8,54>
        modified_method = diffs[6]
        self.assertTrue(modified_method.renamed == modified_method.added == modified_method.removed == False)
        self.assertTrue(modified_method.modified)
        self.assertEquals('login(String,String,AsyncHttpResponseHandler)', modified_method.version_a.name)
        self.assertEquals('login(String,String,AsyncHttpResponseHandler)', modified_method.version_b.name)
        self.assertEquals('API', modified_method.version_b.parent.name)

        # removed class SOAPAPI<55,59>,None in API.java<2,59>
        removed_class = diffs[7]
        self.assertTrue(removed_class.renamed == removed_class.added == removed_class.modified == False)
        self.assertTrue(removed_class.removed)
        self.assertEquals('SOAPAPI', removed_class.version_a.name)
        self.assertEquals(None, removed_class.version_b)
        self.assertEquals('API.java', removed_class.version_a.parent.name)

        # removed method login(String)<56,58>,None in SOAPAPI<55,59>
        removed_method = diffs[8]
        self.assertTrue(removed_method.renamed == removed_method.added == removed_method.modified == False)
        self.assertTrue(removed_method.removed)
        self.assertEquals('login(String)', removed_method.version_a.name)
        self.assertEquals(None, removed_method.version_b)
        self.assertEquals('SOAPAPI', removed_method.version_a.parent.name)

        # removed method register(String,String,String,String,String,String,String,AsyncHttpResponseHandler)<37,47>,None in API<8,53>
        removed_method = diffs[9]
        self.assertTrue(removed_method.renamed == removed_method.added == removed_method.modified == False)
        self.assertTrue(removed_method.removed)
        self.assertEquals('register(String,String,String,String,String,String,String,AsyncHttpResponseHandler)', removed_method.version_a.name)
        self.assertEquals(None, removed_method.version_b)
        self.assertEquals('API', removed_method.version_a.parent.name)

        ##
        # Third commit
        self.assertEqual(repository.commits[2].message, "Third commit\n")
        diffs = sorted(repository.commits[2].diffs)
        self.assertEqual(5, len(diffs))

        # added class None,CallingMethodsInSameClass<7,23> in CallingMethodsInSameClass.java<7,23>
        added_class = diffs[0]
        self.assertTrue(added_class.renamed == added_class.modified == added_class.removed == False)
        self.assertTrue(added_class.added)
        self.assertEquals(None, added_class.version_a)
        self.assertEquals('CallingMethodsInSameClass', added_class.version_b.name)
        self.assertEquals('CallingMethodsInSameClass.java', added_class.version_b.parent.name)

        # added file None,CallingMethodsInSameClass.java
        added_file = diffs[1]
        self.assertTrue(added_file.renamed == added_file.modified == added_file.removed == False)
        self.assertTrue(added_file.added)
        self.assertEquals(None, added_file.version_a)
        self.assertEquals('CallingMethodsInSameClass.java', added_file.version_b.name)
        self.assertEquals(None, added_file.version_b.parent)

        # added method None,main(String)<9,13> in CallingMethodsInSameClass<7,23>
        added_method = diffs[2]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('main(String)', added_method.version_b.name)
        self.assertEquals('CallingMethodsInSameClass', added_method.version_b.parent.name)

        # added method None,printOne()<15,17> in CallingMethodsInSameClass<7,23>
        added_method = diffs[3]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('printOne()', added_method.version_b.name)
        self.assertEquals('CallingMethodsInSameClass', added_method.version_b.parent.name)

        # added method None,printTwo()<19,22> in CallingMethodsInSameClass<7,23>
        added_method = diffs[4]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('printTwo()', added_method.version_b.name)
        self.assertEquals('CallingMethodsInSameClass', added_method.version_b.parent.name)

        ##
        # Fourth commit
        self.assertEqual(repository.commits[3].message, "Fourth commit\n")
        diffs = sorted(repository.commits[3].diffs)
        self.assertEqual(2, len(diffs))

        # removed file CallingMethodsInSameClass.java,None
        removed_file = diffs[0]
        self.assertTrue(removed_file.renamed == removed_file.modified == removed_file.added == False)
        self.assertTrue(removed_file.removed)
        self.assertEquals('CallingMethodsInSameClass.java', removed_file.version_a.name)
        self.assertEquals(None, removed_file.version_b)

        # renamed file API.java,API2.java
        renamed_file = diffs[1]
        self.assertTrue(renamed_file.added == renamed_file.modified == renamed_file.removed == False)
        self.assertTrue(renamed_file.renamed)
        self.assertEquals('API.java', renamed_file.version_a.name)
        self.assertEquals('API2.java', renamed_file.version_b.name)
        self.assertEquals(None, renamed_file.version_b.parent)

        ##
        # Sixth commit
        self.assertEqual(repository.commits[4].message, "Sixth commit\n")
        diffs = sorted(repository.commits[4].diffs)
        self.assertEqual(5, len(diffs))

        # added class None,FirstLevel<5,14> in ShadowTest<1,21>
        added_class = diffs[0]
        self.assertTrue(added_class.renamed == added_class.modified == added_class.removed == False)
        self.assertTrue(added_class.added)
        self.assertEquals(None, added_class.version_a)
        self.assertEquals('FirstLevel', added_class.version_b.name)
        self.assertEquals('ShadowTest', added_class.version_b.parent.name)

        # added class None,ShadowTest<1,21> in ShadowTest.java<1,21>
        added_class = diffs[1]
        self.assertTrue(added_class.renamed == added_class.modified == added_class.removed == False)
        self.assertTrue(added_class.added)
        self.assertEquals(None, added_class.version_a)
        self.assertEquals('ShadowTest', added_class.version_b.name)
        self.assertEquals('ShadowTest.java', added_class.version_b.parent.name)

        # added file None,ShadowTest.java
        added_file = diffs[2]
        self.assertTrue(added_file.renamed == added_file.modified == added_file.removed == False)
        self.assertTrue(added_file.added)
        self.assertEquals(None, added_file.version_a)
        self.assertEquals('ShadowTest.java', added_file.version_b.name)
        self.assertEquals(None, added_file.version_b.parent)

        # added method None,main(String)<16,20> in ShadowTest<1,21>
        added_method = diffs[3]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('main(String)', added_method.version_b.name)
        self.assertEquals('ShadowTest', added_method.version_b.parent.name)

        # added method None,methodInFirstLevel(int)<9,13> in FirstLevel<5,14>
        added_method = diffs[4]
        self.assertTrue(added_method.renamed == added_method.modified == added_method.removed == False)
        self.assertTrue(added_method.added)
        self.assertEquals(None, added_method.version_a)
        self.assertEquals('methodInFirstLevel(int)', added_method.version_b.name)
        self.assertEquals('FirstLevel', added_method.version_b.parent.name)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

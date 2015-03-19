<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Schwa</title>
    <script src="static/d3.min.js"></script>
    <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Open+Sans:400,600">
    <link rel="stylesheet" type="text/css" href="static/styles.css"/>
</head>
<body>

<div id="main">
    <div id="sequence"></div>
    <div id="chart">
        <div id="explanation" style="visibility: hidden;">
            <span id="name"></span> <br/>
            <span id="percentage"></span><br/>
            of defect probability <br/>
            <div class="metrics">
                <span id="revisions"></span>,
                <span id="fixes"></span> <br/>
                and <span id="authors"></span>
            </div>
        </div>
    </div>
    <div class="path">
        <span id="path"></span>
    </div>
</div>



<script type="text/javascript" src="static/app.js"></script>

</body>
</html>

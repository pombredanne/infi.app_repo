<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title></title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="">
        <meta name="author" content="">
        <!-- Le styles -->
        <link href="/assets/css/bootstrap.css" rel="stylesheet">
        <style>
            body {
                padding-top: 60px;
                  /* 60px to make the container go all the way to the bottom of the topbar */
            }
            .big-code {
                font-size: 150%;
            }
        </style>
        <link href="/assets/css/bootstrap-responsive.css" rel="stylesheet">
        <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
        <!--[if lt IE 9]>
            <script src="http://html5shim.googlecode.com/svn/trunk/html5.js">

            </script>
        <![endif]-->
        <!-- Le fav and touch icons -->
        <link rel="shortcut icon" href="/favicon.ico">
        <link rel="apple-touch-icon-precomposed" sizes="144x144" href="/assets/ico/apple-touch-icon-144-precomposed.png">
        <link rel="apple-touch-icon-precomposed" sizes="114x114" href="/assets/ico/apple-touch-icon-114-precomposed.png">
        <link rel="apple-touch-icon-precomposed" sizes="72x72" href="/assets/ico/apple-touch-icon-72-precomposed.png">
        <link rel="apple-touch-icon-precomposed" href="/assets/ico/apple-touch-icon-57-precomposed.png">
        <style>
            undefined
        </style>
    </head>
    <body>
        <div class="navbar navbar-fixed-top navbar-inverse">
            <div class="navbar-inner">
                <div class="container-fluid">
                    <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                        <span class="icon-bar">
                        </span>
                        <span class="icon-bar">
                        </span>
                        <span class="icon-bar">
                        </span>
                    </a>
                    <a class="brand" href="#"></a>
                </div>
            </div>
        </div>
        <form method="post">
            <div class="container-fluid">
                <div class="row-fluid">
                    <div class="span2"></div>
                    <div class="span8">
                        <button type="submit" class="btn">submit</button>
                        <div class="span12">
                            <h1>New packages</h1>
                        </div>
                        % for filepath in missing_packages:
                        <div class="span12">
                            <label class="checkbox">
                                <input type="checkbox" name="${filepath}">
                                    ${filepath.split('/')[-1].rsplit('.',1)[0]}
                                </input>
                            </label>
                        </div>
                        % endfor
                        <div class="span12">
                            <h1>Old packages</h1>
                        <div>
                        % for filepath in ignored_packages:
                        <div class="span12">
                            <label class="checkbox">
                                <input type="checkbox" name="${filepath}">
                                    ${filepath.split('/')[-1].rsplit('.',1)[0]}
                                </input>
                            </label>
                        </div>
                        % endfor
                        </div>
                    </div>
                    <div class="span2"></div>
                </div>
            </div>
        </form>
        <script src="/static/jquery-1.8.1.min.js"></script>
        <script src="/static/jquery.dataTables.min.js"></script>
        <script src="/assets/js/bootstrap.js"></script>

    </body>
</html>

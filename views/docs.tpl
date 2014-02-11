<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{{title}}</title>

    <link rel="stylesheet" href="/css/ink-min.css">

    <script src="/js/zepto.min.js"></script>
    <script src="/js/marked.js"></script>

    <script>
        $(document).ready(function () { 
            $('.docstring').each(function() {
                $(this).html(marked($(this).text()))
            })
        });
        
    </script>
  </head>

<div id="topbar">
  <nav class="ink-navigation ink-grid">
    <ul class="menu horizontal flat black shadowed">
      <li><a href="#">{{title}}</a></li>
    </ul>
  </nav>
</div>

  <div class="ink-grid">
%for item in docs:
%if item['doc'][0] != "#": # skip our template docstrings
<section class="vertical-space">
    <h3>{{item['function'].title()}}</h3>
    <tt>{{item['method']}} {{item['route']}}</tt>
    <div class="docstring">{{item['doc']}}</div>
</section>
%end
%end
  </div>
  </body>
</html>

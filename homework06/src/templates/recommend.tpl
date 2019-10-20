<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui three item menu">
          <a class="item" href="/classify">Разметить</a>
          <a class="active item" disabled>Рекомендовать</a>
        </div>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Заголовок</th>
            </thead>
            <%
                labels = {
                    -1: "negative",
                    0: "active",
                    1: "positive"
                }
            %>
            <tbody>
                %for row in rows:
                    <tr>
                        <td class={{labels[row[1]]}}><a href="{{ row[0].url }}">{{ row[0].title }}</a></td>
                    </tr>
                %end
            </tbody>
        </table>
        </div>
    </body>
</html>

<!-- news_template.tpl -->
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.css"></link>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/components/breadcrumb.css" />
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.12/semantic.min.js"></script>
    </head>
    <body>
        <div class="ui three item menu">
          <a class="active item" disabled>Разметить</a>
          <a class="item" href="/recommend">Рекомендовать</a>
        </div>
        <div class="ui container" style="padding-top: 10px;">
        <table class="ui celled table">
            <thead>
                <th>Заголовок</th>
                <th>Автор</th>
                <th>Оценки</th>
                <th>Комментарии</th>
                <th colspan="3">Метка</th>
            </thead>
            <tbody>
                %for row in rows:
                <tr>
                    <td><a href="{{ row.url }}">{{ row.title }}</a></td>
                    <td>{{ row.author }}</td>
                    <td>{{ row.points }}</td>
                    <td>{{ row.comments }}</td>
                    <td class="positive"><a href="/add_label?label=good&id={{ row.id }}">Интересно</a></td>
                    <td class="active"><a href="/add_label?label=unsure&id={{ row.id }}">Возможно</a></td>
                    <td class="negative"><a href="/add_label?label=bad&id={{ row.id }}">Не интересно</a></td>
                </tr>
                %end
            </tbody>
            <tfoot class="full-width">
                <tr>
                    <th colspan="7">
                        <a href="/update_news" class="ui right floated small primary button">Больше новостей!</a>
                    </th>
                </tr>
            </tfoot>
        </table>
        </div>
    </body>
</html>

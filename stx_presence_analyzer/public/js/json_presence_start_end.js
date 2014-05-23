(function($) {
    $(document).ready(function(){
        var loading = $('#loading');
        $.getJSON("/users", function(result) {
            var dropdown = $("#user_id");
            $.each(result, function(item) {
                dropdown.append($("<option />").val(this.user_id).text(this.name));
            });
            dropdown.show();
            loading.hide();
        });
        $('#user_id').change(function(){
            var selected_user = $("#user_id").val();
            var chart_div = $('#chart_div');
            var photo = $('#photo');
            
            if(selected_user) {
                loading.show();
                chart_div.hide();
                photo.hide();
                // $.getJSON("/"+selected_user,  function(result) {
                //     $.each(result, function(index, value) {
                //         value[1] = new Date(value[1] * 1000);
                //         value[2] = new Date(value[2] * 1000);
                //     });

                //     var data = new google.visualization.DataTable();
                //     data.addColumn('string', 'Weekday');
                //     data.addColumn({ type: 'datetime', id: 'Start' });
                //     data.addColumn({ type: 'datetime', id: 'End' });
                //     data.addRows(result);
                //     var options = {
                //         hAxis: {title: 'Weekday'}
                //     };
                //     var formatter = new google.visualization.DateFormat({pattern: 'HH:mm:ss'});
                //     formatter.format(data, 1);
                //     formatter.format(data, 2);

                //     chart_div.show();

                //     var url = "https://intranet.stxnext.pl/api/images/users/";
                //     photo.html('<img src="' + url + selected_user +'" alt="Error" />');
                //     photo.show();

                //     loading.hide();
                //     var chart = new google.visualization.Timeline(chart_div[0]);
                //     chart.draw(data, options);
                // });
            }
        });
    });
})(jQuery);
(function($) {
    $(document).ready(function(){
        var loading = $('#loading');
        $.getJSON("", function(result) {
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
                
                $.getJSON("/"+selected_user, function(result) {
                    var data = google.visualization.arrayToDataTable(result);
                    var options = {};
                    chart_div.show();

                    var url = "https://intranet.stxnext.pl/api/images/users/";
                    photo.html('<img src="' + url + selected_user +'" alt="Error" />');
                    photo.show();

                    loading.hide();
                    var chart = new google.visualization.PieChart(chart_div[0]);
                    chart.draw(data, options);
                });
            }
        });
    });
})(jQuery);
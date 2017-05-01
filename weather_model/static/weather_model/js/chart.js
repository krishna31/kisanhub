$(function(){
        $("#frm_details").on("submit", function(event) {
            event.preventDefault();

            var element_year = document.getElementsByName("year")[0];
            var year = element_year.options[element_year.selectedIndex].value;

            var element_value_type = document.getElementsByName("value_type")[0];
            var value_type = element_value_type.options[element_value_type.selectedIndex].value;

            var formData = {
                'year': year,
                'value_type': value_type,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            };
            console.log(formData);
            $.ajax({
                url: "/chart/",
                type: "post",
                data: formData,
                success: function(data) {
                   console.log(data)
                    var nctx = document.getElementById("newChart").getContext('2d');
                    var newchart = new Chart(nctx, {'type': 'line', 'data': data.data});
                }
            });
        });
    })
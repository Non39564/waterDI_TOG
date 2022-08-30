
var minDate, maxDate;
 
// Custom filtering function which will search data in column four between two values
$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        var min = minDate.val();
        var max = maxDate.val();
        var date = new Date( data[4] );
 
        if (
            ( min === null && max === null ) ||
            ( min === null && date <= max ) ||
            ( min <= date   && max === null ) ||
            ( min <= date   && date <= max )
        ) {
         console.log("min"+min)
         console.log("max"+max)
         console.log("date"+date)
            return true;
        }
        return false;
    }
);
 
$(document).ready(function() {
    // Create date inputs
    minDate = new DateTime($('#min'), {
        format: 'MMMM Do YYYY'
    });
    maxDate = new DateTime($('#max'), {
        format: 'MMMM Do YYYY'
    });
 
    // DataTables initialisation
    var table = $('#line').DataTable({
        pagingType: 'full_numbers',
        scrollY: '1000px',
        scrollCollapse: true,
        pageLength: 20,
        lengthMenu: [ [20, 30, 40, 50, -1], [20, 30, 40, 50, "All"] ],
        dom: 'Blfrtip',
        buttons: [
          {
            extend: 'excel',
            text: '<i class="fa fa-file-excel me-2"></i><span>generate excel</span>',
            className: 'mb-3 btn btn-success me-1',
          }
      ],
      });
 
    // Refilter the table
    $('#min, #max').on('change', function () {
        table.draw();
        console.log("change")
    });
});

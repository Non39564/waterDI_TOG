// Table Phase 5
var minDateP5, maxDateP5;
 
 // Custom filtering function which will search data in column four between two values
 $.fn.dataTable.ext.search.push(
     function( settings, data, dataIndex ) {
         var min = minDateP5.val();
         var max = maxDateP5.val();
         var date = new Date( data[0] );
  
         if (
             ( min === null && max === null ) ||
             ( min === null && date <= max ) ||
             ( min <= date   && max === null ) ||
             ( min <= date   && date <= max )
         ) {
             return true;
         }
         return false;
     }
 );
  
 $(document).ready(function() {
     // Create date inputs
     minDateP5 = new DateTime($('#minP5'), {
         format: 'MMMM Do YYYY'
     });
     maxDateP5 = new DateTime($('#maxP5'), {
         format: 'MMMM Do YYYY'
     });
  
     // DataTables initialisation
     var table = $('#P5').DataTable();
  
     // Refilter the table
     $('#minP5, #maxP5').on('change', function () {
         table.draw();
     });
 });
//End Table Phase 5
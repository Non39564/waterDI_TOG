// Phase 4
var minDate4, maxDate4;
var minDate5, maxDate5;

 // Custom filtering function which will search data in column four between two values
 $.fn.dataTable.ext.search.push(
     function( settings, data, dataIndex ) {
         var min4 = minDate4.val();
         var max4 = maxDate4.val();
         var min5 = minDate5.val();
         var max5 = maxDate5.val();
         var date = new Date( data[0] );
         
         if (
             ( min4 === null && max4 === null ) ||
             ( min4 === null && date <= max4 ) ||
             ( min4 <= date   && max4 === null ) ||
             ( min4 <= date   && date <= max4 )
         ) {
             return true;
         } if (
            ( min5 === null && max5 === null ) ||
            ( min5 === null && date <= max5 ) ||
            ( min5 <= date   && max5 === null ) ||
            ( min5 <= date   && date <= max5 )
         ) {
            return true;
         }
         return false;
     }
 );
  
 $(document).ready(function() {
     // Create date inputs
     minDate4 = new DateTime($('#minP4'), {
         format: 'Do MMMM YYYY'
     });
     maxDate4 = new DateTime($('#maxP4'), {
         format: 'Do MMMM YYYY'
     });
     minDate5 = new DateTime($('#minP5'), {
         format: 'Do MMMM YYYY'
     });
     maxDate5 = new DateTime($('#maxP5'), {
         format: 'Do MMMM YYYY'
     });
     // DataTables initialisation
     var tableP4 = $('#P4').DataTable();
     var tableP5 = $('#P5').DataTable();
    //  var tableP9 = $('#P9').DataTable();
  
     // Refilter the table
     $('#minP4, #maxP4').on('change', function () {
         tableP4.draw();
     });
     $('#minP5, #maxP5').on('change', function () {
         tableP5.draw();
     });
    //  $('#minP9, #maxP9').on('change', function () {
    //      tableP4.draw();
    //  });
 });

//  Phase 5
// var minDate5, maxDate5;

// $.fn.dataTable.ext.search.push(
//     function( settings, data, dataIndex ) {
//         var min = minDate5.val();
//         var max = maxDate5.val();
//         var date = new Date( data[0] );
 
//         if (
//             ( min === null && max === null ) ||
//             ( min === null && date <= max ) ||
//             ( min <= date   && max === null ) ||
//             ( min <= date   && date <= max )
//         ) {
//             return true;
//         }
//         return false;
//     }
// );
 
// $(document).ready(function() {
//     minDate5 = new DateTime($('#minP5'), {
//         format: 'Do MMMM YYYY'
//     });
//     maxDate5 = new DateTime($('#maxP5'), {
//         format: 'Do MMMM YYYY'
//     });

//     var table = $('#P5').DataTable();

//     $('#minP5, #maxP5').on('change', function () {
//         table.draw();
//     });
// });

// Phase 9

// var minDate9, maxDate9;

// $.fn.dataTable.ext.search.push(
//     function( settings, data, dataIndex ) {
//         var min9 = minDate9.val();
//         var max9 = maxDate9.val();
//         var date9 = new Date( data[0] );
 
//         if (
//             ( min9 === null && max9 === null ) ||
//             ( min9 === null && date9 <= max9 ) ||
//             ( min9 <= date9   && max9 === null ) ||
//             ( min9 <= date9   && date9 <= max9 )
//         ) {
//             return true;
//         }
//         return false;
//     }
// );
 
// $(document).ready(function() {
    
//     minDate9 = new DateTime($('#minP9'), {
//         format: 'Do MMMM YYYY'
//     });
//     maxDate9 = new DateTime($('#maxP9'), {
//         format: 'Do MMMM YYYY'
//     });
 
   
//     var table9 = $('#P9').DataTable({
//         pagingType: 'full_numbers',
//         scrollY: '200px',
//         scrollCollapse: true,
//         pageLength: 5,
//         lengthMenu: [ [5, 10, 25, 50, -1], [5, 10, 25, 50, "All"] ],
//       });
 
   
//     $('#minP9, #maxP9').on('change', function () {
//         table9.draw();
//     });
// });
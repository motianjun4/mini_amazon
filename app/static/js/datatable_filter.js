
$(()=>{
    if (window.datatables["product-search-list"]){
        yadcf.init(window.datatables["product-search-list"], [
          { column_number: 1, filter_type: "range_number_slider" },
          { column_number: 2, filter_type: "range_number_slider" },
          { column_number: 3, filter_type: "range_number_slider" },
        ]);
    }
})
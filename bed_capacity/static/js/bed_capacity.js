// Script for fetching wilayah data from database
$(document).ready(function() {
    console.log("fetching wilayah data");
    $.ajax({
        url:"wilayah_json",
        dataType: 'json',
        success: function(res) {
            $.each(res, function(i, wilayah) {
                var option = $(`<option value="${wilayah.pk}">${wilayah.fields.nama}</option>`);
                $("#select-wil").append(option);
            });
        }
    });

    // Ketika fetch sudah sukses, baru kita ubah laman
    if (sessionStorage.getItem('selectedWil') != null) {
        $(document).ready(function() {
            setTimeout(function() {
                $("#select-wil").val( sessionStorage.getItem('selectedWil'));
                getHospData();
                //$('#search-btn').trigger('click');
            }, 1000);
        });
    }
});

// function for fetching hospital data (after choosing wilayah)
function getHospData() {
    var selectedWil = $("#select-wil").val();

        // Simpan state wilayah sekarang agar tidak hilang ketika direfresh
        sessionStorage.setItem('selectedWil', selectedWil);

        $.ajax({
            url: "bed_data_json/wil/" + selectedWil,
            dataType: "json",
            success: function(res) {
                $('#table-content').empty();

                $.each(res, function(i, rs) {
                    console.log('didapat pjg:' + res.length)
                    console.log('masuk, res.length= ' + res.length)
                    var row = $(`<div class="rs-data row" id="rs-${rs.pk}"></div>`);
                    var c1 = $('<div class="col-md-9"></div>');
                    var c2 = $('<div class="col-md-3"></div>');
    
                    if (rs.fields.kapasitas <= rs.fields.isi) {
                        c1.append(`<h5 style='color: #9a9a9a;'>${rs.fields.nama}</h5>`);
                    } else {
                        c1.append(`<h5>${rs.fields.nama}</h5>`);
                    }
                    c1.append(`<p>${rs.fields.alamat}</p>`);
                    c2.append(`<h5>${rs.fields.isi}/${rs.fields.kapasitas}</h5>`);
    
    
                    row.append(c1);
                    row.append(c2);
    
                    // Skrip jika row rumah sakit ditekan
                    $(row).on('click', function() {
                        var id = $(this).attr('id').slice(3);
                        console.log(`sukses ${id}`)
                        $.ajax({
                            url: `bed_data_json/${id}`,
                            dataType: 'json',
                            success: function(res) {
                                res = res[0];
                                // Fetch data
                                $('#selected-nama').html(res.fields.nama);
                                $('#selected-nama-title').html(res.fields.nama);
                                $('#selected-alamat').html(res.fields.alamat);
                                $('#selected-telp').html(res.fields.telp);
                                $('#selected-kapasitas').html(res.fields.kapasitas);
                                $('#rs_input').val(res.pk);
                                $('#rs_name').val(res.fields.nama);
    
                                console.log('masuk sini');
                                // Cek apakah rumah sakit penuh atau tidak
                                if (rs.fields.kapasitas <= rs.fields.isi) {
                                    $('#request-btn').attr('class', 'btn btn-outline-secondary');
                                    $('#request-btn').attr('data-toggle', '');
                                    $('#request-btn').attr('data-target', '');
                                } else {
                                    // Lakukan toggle tombol request agar bisa ditekan jika tidak penuh
                                    $('#request-btn').attr('class', 'btn btn-success');
                                    $('#request-btn').attr('data-toggle', 'modal');
                                    $('#request-btn').attr('data-target', '#exampleModalCenter');
                                }
                            }
                        })
                    });

                    $("#table-content").append(row);
                });

                // Jika wilayah tak ada rs
                if (res.length == 0) {
                    $('#table-content').append(`
                        <div style="text-align: center; height: 350px; vertical-align: middle; padding-top: 100px;">
                        <h1 style="color: #cdcdcd;"> :( </h1>
                        <h5 style="color: #cdcdcd;">Belum ada rumah sakit terdaftar di ${$("#select-wil :selected").text()}</h5>
                        </div>
                        `);
                }
            }
        });
}

// Script for calling getWilData() if change is detected
$(document).ready(function() {
    //$('#search-btn').on('click', function() {
    $('#select-wil').change(function() {
        getHospData();
    });
    
    console.log("success fetching data");
    
})

// Script that prevents user from clicking button before selecting hospital
$(document).ready(function() {
    $('#request-btn').click(function() {
        if ($(this).attr('class') == 'btn btn-light') {
            alert("Mohon pilih rumah sakit terlebih dahulu!");
        } else if ($(this).attr('class') == 'btn btn-outline-secondary') {
            alert("Rumah sakit terpilih sudah penuh kapasitasnya!");
        }
    });
});

// Script for UX: confirming new request successfully made
$(document).ready(function() {
    if (sessionStorage.getItem('has-been-here') == 1) {
        sessionStorage.setItem('has-been-here', 0);
        $('#nama-req-last').html(sessionStorage.getItem('nama-req-last'));
        $('#nama-rs-last').html(sessionStorage.getItem('nama-rs-last'));
        $('#exampleModalCenter1').modal('show');
    }
});

// Script for closing modal
$(document).ready(function() {
    $('#close-btn').on('click', function() {
        $('#exampleModalCenter1').modal('hide');
    })
});
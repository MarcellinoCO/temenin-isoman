// Script for fetching wilayah data from database
$(document).ready(function() {
    console.log("... fetching wilayah data");
    $.ajax({
        url:"wilayah_json",
        dataType: 'json',
        success: function(res) {
            $.each(res, function(i, wilayah) {
                var option = $(`<option value="${wilayah.pk}">${wilayah.fields.nama}</option>`);
                $("#select-wil").append(option);
            });
            console.log("success fetching wilayah data ...");
        }
    });
});

// Function for fetching hospital data from database (after selecting wilayah)
function getHospData() {
    console.log("... fetching rs data");
    var selectedWil = $("#select-wil").val();
    var firstRS;

    if (selectedWil == '---') {
        alert("Silakan pilih wilayah terlebih dahulu!");
        return;
    }

    // Set state supaya laman tidak hilang ketika di-refresh
    sessionStorage.setItem('selectedWil', selectedWil);

    $.ajax({
        url:"bed_data_json/wil/" + selectedWil,
        dataType: 'json',
        success: function(res) {
            firstRS = res[0].pk;

            $('#select-rs').empty();

            $.each(res, function(i, rs) {
                var option = $(`<option value="${rs.pk}">${rs.fields.nama}</option>`);
                $("#select-rs").append(option);

            $('#select-rs').val(firstRS).change();
            sessionStorage.setItem('selectedRS', firstRS);
            });

            console.log("success fetching rs data ...");

            // Ketika fetch sudah sukses, baru kita ubah laman
            if (sessionStorage.getItem('selectedRS') != null) {
                $(document).ready(function() {
                    setTimeout(function() {
                        $("#select-rs").val(sessionStorage.getItem('selectedRS'));
                        $('#search-btn').trigger('click');
                    }, 250);
                });
            }
        }
    });
}

// Script for calling getHospData if change is detected
$(document).ready(function() {
    // Start fetching on search btn click
    $('#select-wil').change(function () {
        getHospData();
    });
 
    // Ketika fetch sudah sukses, baru kita ubah laman
    if (sessionStorage.getItem('selectedWil') != null) {
        $(document).ready(function() {
            setTimeout(function() {
                $("#select-wil").val(sessionStorage.getItem('selectedWil'));
                //$('#search-btn-1').trigger('click');
            }, 250);
        });
    }
});

// After selecting hospital, this script runs to fetch requesters data from selected hospital
$(document).ready(function() {
    $("#search-btn").on('click', function() {
    //$("#select-rs").change(function() {
        console.log("... fetching requesters data");
        var selectedRS = $("#select-rs").val();

        if (selectedRS == '---') {
            alert("Silakan pilih rumah sakit terlebih dahulu!");
            return;
        }

        // Set state supaya laman tidak hilang ketika di-refresh
        sessionStorage.setItem('selectedRS', selectedRS);

        // Ajax untuk fetch informasi rumah sakit
        $.ajax({
            url: 'bed_data_json/' + selectedRS,
            dataType: 'json',
            success: function(res) {
                var rs = res[0]
                $('#id-kapasitas').val(rs.fields.kapasitas);
                $('#id-isi').val(rs.fields.isi);
                $('#indikator-kapasitas').html(rs.fields.isi + ' / ' + rs.fields.kapasitas);
                $('#kode-rs').val(rs.pk);
            }
        })

        // Ajax untuk fetch data request di rumah sakit tersebut
        $.ajax({
        url: `request_data_json/${selectedRS}`,
        dataType: "json",
        success: function(res) {
            $('#table-content').empty();

            if (res.length != 0) {
                $.each(res, function(i, rq) {
                    var row = $(`<div class="requester-data row" id="rq-${rq.pk}"></div>`);
                    var c1 = $('<div class="col-md-10"></div>');
                    var c2 = $('<div class="col-md-2"></div>');

                    var btn_acc = $(`<button type="button" class="btn btn-success btn-sm" id="ac-${rq.pk}">Acc</button>`)
                    btn_acc.click(function() {
                        // Set teks modal
                        $('#nama-aksi').html('menambahkan');
                        $('#nama-rs').html($("#select-rs :selected").text());
                        $('#nama-pasien').html(rq.fields.nama);

                        // Set dan show modal
                        $('#kode-aksi').val('acc');
                        $('#kode-request').val(rq.pk);
                        $('#exampleModalCenter').modal('show');
                    });

                    var btn_dec = $(`<button type="button" class="btn btn-danger btn-sm" id="de-${rq.pk}">Dec</button>`)
                    btn_dec.click(function() {
                        // Set teks modal
                        $('#nama-aksi').html('menolak');
                        $('#nama-rs').html($("#select-rs :selected").text());
                        $('#nama-pasien').html(rq.fields.nama);

                        // Set dan show modal
                        $('#kode-aksi').val('acc');
                        $('#kode-request').val(rq.pk);
                        $('#exampleModalCenter').modal('show');
                    });

                    var btn_container = $('<div class="btn-group" role="group" aria-label="Basic example"></div>')
                    btn_container.append(btn_acc);
                    btn_container.append(btn_dec);


                    c1.append(`
                    <h5>${rq.fields.nama}</h5>
                    <p>${rq.fields.gender == 'L' ? 'Laki-laki' : 'Perempuan'}, ${rq.fields.umur} tahun</p>
                    <ul>
                        <li>${rq.fields.telp}</li>
                        <li>${rq.fields.alamat}</li>   
                    </ul>
                    `);
                    c2.append(btn_container);
                    
                    row.append(c1);
                    row.append(c2);

                    $("#table-content").append(row);
                });
                console.log("success fetching requesters data ...");
            } else {
                $('#table-content').append(`
                <div style="text-align: center; height: 350px; vertical-align: middle; padding-top: 100px;">
                <h1 style="color: #cdcdcd;"> :) </h1>
                <h5 style="color: #cdcdcd;">Belum ada request terbaru dari ${$("#select-rs :selected").text()}</h5>
                </div>
                `)
            }
        }
    });

    });
});

// Script that enables modal to be closed
$(document).ready(function() {
    $('#batal-btn').on('click', function() {
        $('#exampleModalCenter').modal('hide');
    });
});

// Script that prevents admin from clicking button before selecting hospital
$(document).ready(function() {
    $('#edit-btn').on('click', function() {
        if ($("#select-rs").val() == '---') {
            alert('Silakan pilih rumah sakit terlebih dahulu!');
        } else {
            $('#exampleModalCenter1').modal('show');
        }
    });

    $('#batal-btn2').on('click', function() {
        $('#exampleModalCenter1').modal('hide');
    });
});
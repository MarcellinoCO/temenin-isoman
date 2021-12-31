$(document).ready(function () {

    $('#pilihDaerah').change(function (e) {
        e.preventDefault();

        $("#container-rumah-sakit").empty();;
        $.ajax({
            url: "daerah_json",
            dataType: 'json',
            success: function (res) {
                $.each(res, function (i, item) {
                    const daerah = $('select[id=pilihDaerah] option').filter(':selected').val()
                    if (item.fields.daerah == daerah) {
                        var option = $(`<tr>
                                        <td style="cursor: pointer" data-bs-toggle="modal" data-bs-target="#rsModal" onclick="telepon('${item.fields.nama}', '${item.fields.telepon}')">${item.fields.nama}<br><small>${item.fields.alamat}</small></td>
                                        <td style="cursor: pointer" data-bs-toggle="modal" data-bs-target="#rsModal" onclick="telepon('${item.fields.nama}', '${item.fields.telepon}')" class="text-center">${item.fields.telepon}</td>
                                        <td style="cursor: pointer" data-bs-toggle="modal" data-bs-target="#editRSModal" onclick="editRs('${item.pk}', '${item.fields.nama}', '${item.fields.alamat}', '${item.fields.telepon}', '${item.fields.daerah}')"><a href="#"><i class="fas fa-pencil-alt"></i></a></td>
                                        <tr>`);
                        $("#container-rumah-sakit").append(option);
                    }
                });
            }
        });
    });

});

function telepon(nama, telepon) {
    $('#rsModalLabel').text(nama);
    $('#kalimat-telepon').text(`Apakah Anda ingin terhubung langsung ke ${nama}?`);
    $('#NomorTelepon').attr('href', `tel:${telepon}`);
}

function editRs(id, nama, alamat, telepon, IDdaerah) {
    const daerah = $('select[id=pilihDaerah] option').filter(':selected').text()

    $('#form-edit-rs').attr('action', `update_rs/${id}/`);
    $('#hapusRs').attr('href', `hapus_rs/${id}/`);
    $('#editRs').text(nama);

    $('#edit-nama').val(nama);
    $('#edit-alamat').val(alamat);
    $('#edit-telepon').val(telepon);
    $('#edit-daerah').text(daerah);
    $('#edit-daerah').val(IDdaerah);
}

function editDaerah(id, nama) {
    $('#update-daerah').attr('action', `update_daerah/${id}/`);
    $('#hapus-daerah').attr('href', `hapus_daerah/${id}/`);
    $('#edit-daerah').text(nama)
    $('#input-daerah').val(nama)
}

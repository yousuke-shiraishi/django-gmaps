function initMap() {
  let addresses = window.addresses;
  console.log("aaaaaaaaaa", addresses);
  const markers = [];
  const map = new google.maps.Map(document.getElementById("gmaps"), {
    zoom: 4,
  });
  const bounds = new google.maps.LatLngBounds();
  const largeInfowindow = addresses.map(
    (address) => new google.maps.InfoWindow({ content: address.comment })
  );

  addresses.forEach((address, i) => {
    const marker = new google.maps.Marker({
      position: {
        lat: parseFloat(address.latitude),
        lng: parseFloat(address.longitude),
      },
      map,
      title: address.title,
      id: address.id,
    });

    markerEvent(i, largeInfowindow, marker, address, map);

    markers.push(marker);
    bounds.extend(marker.position);
  });

  map.fitBounds(bounds);
}

const rebuildcomment = (str, length) => {
  if (!str || !length || length < 1) return [];

  const resultArr = [];
  let start = 0;
  let end = length;

  while (start < str.length) {
    resultArr.push(str.substring(start, end));
    start = end;
    end = start + length;
  }

  return resultArr.join("<br>");
};

const markerEvent = (i, largeInfowindow, marker, address, map) => {
  marker.addListener("click", () => {
    if (largeInfowindow[i].marker !== marker) {
      largeInfowindow[i].marker = marker;
      largeInfowindow[i].content = rebuildcomment(
        largeInfowindow[i].content,
        30
      );

      const { url } = address.image;
      const { id, title } = largeInfowindow[i].marker;
      largeInfowindow[i].setContent(
        `<a href="${url}" target="_blank" data-lightbox="image-${id}">
             <img class="picture" src="${url}" alt="" width="150px" height="auto"/>
           </a>
           <div><p>${title}</p></div>
           <div><p>${largeInfowindow[i].content}</p></div>
           <div><input type="button" value="マーカーを削除する" id="btn${id}"/></div>`
      );

      largeInfowindow[i].open(map, marker);

      const target = `#btn${id}`;
      $(document).on("click", target, () => {
        if (confirm("本当に削除しますか?削除すると戻せません。")) {
          const CSRF_TOKEN = $('meta[name="csrf-token"]').attr("content");

          $.ajax({
            url: `/gmaps/delete/?q=${id}`,
            type: "DELETE",
            data: { _token: CSRF_TOKEN },
            processData: false,
            contentType: false,
            dataType: "json",
          })
            .then(() => {
              alert("削除に成功しました。");
              marker.setMap(null);
            })
            .catch(() => {
              alert("他の人のマーカー情報は消せません。");
            });
        }
      });
    }
  });
};

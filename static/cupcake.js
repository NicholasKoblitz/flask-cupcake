async function displayCupcakes() {
    let cupcakes = await axios.get("/api/cupcakes");
    for(let cupcake of cupcakes.data.cupcakes) {
        $("#cupcake-list").append(`
            <li data-id=${cupcake.id}>
                <li>${cupcake.flavor}</li>
                <li><img src='${cupcake.image}' style= "width: 200px;  height: 200px"></li>
                <li>${cupcake.size}</li>
                <li>${cupcake.rating}</li>
            </li>
        `);
    }

}

async function CreateCupcake(evt) {
    evt.preventDefault()
  
    newCupcake = await axios({
        method: "post",
        url: "/api/cupcakes",
        data: {
            flavor: $("#flavor").val(),
            size: $("#size").val(),
            rating: $("#rating").val(),
            image: $("#image").val()
        }
    });
    $("form").trigger("reset")
    

    cupcake = await axios.get(`/api/cupcakes/${newCupcake.data.cupcake.id}`)

    console.log(cupcake)

    $("#cupcake-list").append(`
    <li data-id=${cupcake.data.cupcake.id}>
        <li>${cupcake.data.cupcake.flavor}</li>
        <li><img src='${cupcake.data.cupcake.image}' style= "width: 200px;  height: 200px"></li>
        <li>${cupcake.data.cupcake.size}</li>
        <li>${cupcake.data.cupcake.rating}</li>
    </li>
`);
}


$("button").click(CreateCupcake)


displayCupcakes()
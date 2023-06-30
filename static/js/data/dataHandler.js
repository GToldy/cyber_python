export let dataHandler = {
    // getBoards: function () {
    //     // promise-t ad vissza, nem kell async, await
    //     return apiGet("/api/boards");
    // },
};

async function apiGet(url) {
    const response = await fetch(url, {
        method: "GET",
    });

    if (response.ok) {
        return await response.json();
    }

    throw new Error(response.status);
}

async function apiPost(url, payload) {
    const response = await fetch(url, {
      method: "POST",
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json",
      },
    });

     if (response.ok) {
        return await response.json();
     }
     throw new Error(response.status);
};

// POST ha létre akarunk hozni vmit a szerveren
// GET
async function apiDelete(url) {
    const response = await fetch(url, {
      method: "DELETE",
    });

     if (response.ok) {
        return await response.json();
     }
     throw new Error(response.status);
}

async function apiPut(url, payload) {
    const response = await fetch(url, {
      method: "PUT",
      body: JSON.stringify(payload),
      headers: {
        "Content-Type": "application/json",
      },
    });

     if (response.ok) {
        return await response.json();
     }
     throw new Error(response.status);
}

async function apiPatch(url) {
}

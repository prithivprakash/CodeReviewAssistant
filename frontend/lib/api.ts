export async function askAssistant(payload:any) {
    const res = await fetch("http://127.0.0.1:8000/ask", {
        method : "POST",
        headers : {
            "Content-type" : "application/json",
        },
        body: JSON.stringify(payload),
        
    });

    if (!res.ok){
        const err = await res.json();
        throw new Error(err.detail || "Something went wrong");
    }

    return res.json();
    
}
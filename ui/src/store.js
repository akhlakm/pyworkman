import { writable } from "svelte/store";

export const alert = writable("");

export const selected_service = writable("");

export const service_list = writable(null);

export const job_status = writable(null);

export const job_list = writable(null);

export const service_details = writable(null);

export const last_response = writable(null);

export function clear() {
    alert.set("");
    job_status.set(null);
    service_details.set(null);
    service_list.set(null);
}

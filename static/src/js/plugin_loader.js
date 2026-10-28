import { loadJS } from "@web/core/assets";

export async function loadJsFile(file_path) {
    const loadFile = await loadJS(file_path);
    return loadFile
}
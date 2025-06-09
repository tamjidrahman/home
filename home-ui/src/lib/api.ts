export async function fetchDeviceStatus(type: string, names?: string[]) {
  const params = names?.length ? `?${type}=${names.join(",")}` : "";
  const res = await fetch(`http://nixos:8000/${type}/status${params}`);
  if (!res.ok) throw new Error(`Failed to fetch ${type} status`);
  return res.json();
}

export async function invokeCommand(type: string, command: string, names?: string[]) {
  const params = names?.length ? `?${type}=${names.join(",")}` : "";
  const res = await fetch(`http://nixos:8000/${type}/${command}${params}`, {
    method: "POST"
  });
  if (!res.ok) throw new Error(`Failed to invoke ${command}`);
  return res.json();
}
export async function fetchDeviceCommands(type: string): Promise<string[]> {
  const res = await fetch(`http://nixos:8000/${type}/commands`)
  if (!res.ok) return []
  return res.json()
}

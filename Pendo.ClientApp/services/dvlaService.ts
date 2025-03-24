const url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles";

export async function validateRegPlate(regPlate: string): Promise<boolean> {
  try {
    // Sanitise the registration plate to remove spaces and non-alphanumeric characters.
    const sanitisePlate = regPlate.replace(/[^A-Za-z0-9]/g, "");

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": process.env.EXPO_PUBLIC_DVLA_KEY || "",
      },
      body: JSON.stringify({ registrationNumber: sanitisePlate }),
    });
    if (response.ok) {
      const data = await response.json();

      // Check if the response contains a registrationNumber indicating a valid plate.
      return !!data.registrationNumber;
    } else {
      const errorData = await response.json();
      console.error("DVLA API error:", errorData);
      return false;
    }
  } catch (error) {
    console.error("DVLA plate validation error:", error);
    return false;
  }
}

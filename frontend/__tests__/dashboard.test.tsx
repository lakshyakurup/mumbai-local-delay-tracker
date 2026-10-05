import { render, screen } from "@testing-library/react";
import { LineStatusCard } from "@/components/LineStatusCard";

describe("line status dashboard", () => {
  it("renders severity and delay telemetry", () => {
    render(<LineStatusCard status={{ line: "Central", status: "major", average_delay_minutes: 16, active_incidents: 4, updated_at: new Date().toISOString() }} />);
    expect(screen.getByText("Central")).toBeInTheDocument();
    expect(screen.getByText("Major disruption")).toBeInTheDocument();
    expect(screen.getByText("16 min late")).toBeInTheDocument();
  });
});

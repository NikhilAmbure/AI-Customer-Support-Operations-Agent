from graph import app
from pathlib import Path

# Generate the graph image
png_data = app.get_graph().draw_mermaid_png()

# Save it to a file
output_path = Path("graph.png")
output_path.write_bytes(png_data)

print(f"Graph image saved to: {output_path.resolve()}")
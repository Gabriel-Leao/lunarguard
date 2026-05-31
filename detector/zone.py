from dataclasses import dataclass


@dataclass
class Zone:
    name: str
    x1: int
    y1: int
    x2: int
    y2: int
    restricted: bool = True


class ZoneManager:
    def __init__(self, frame_w: int, frame_h: int):
        self.zones: list[Zone] = [
            Zone(
                name="Nucleo de Controle",
                x1=int(frame_w * 0.02),
                y1=int(frame_h * 0.05),
                x2=int(frame_w * 0.22),
                y2=int(frame_h * 0.35),
                restricted=True,
            ),
            Zone(
                name="Reator de Energia",
                x1=int(frame_w * 0.78),
                y1=int(frame_h * 0.65),
                x2=int(frame_w * 0.98),
                y2=int(frame_h * 0.95),
                restricted=True,
            ),
        ]

    def check_intrusion(self, boxes: list[tuple]) -> list[tuple[Zone, tuple]]:
        intrusions = []
        for box in boxes:
            bx, by, bw, bh = box
            for zone in self.zones:
                if not zone.restricted:
                    continue
                if (
                    bx < zone.x2
                    and bx + bw > zone.x1
                    and by < zone.y2
                    and by + bh > zone.y1
                ):
                    intrusions.append((zone, box))
        return intrusions

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
    """
    Gerencia zonas de segurança definidas no frame.
    Verifica se um bounding box de movimento intersecta uma zona restrita.
    """

    def __init__(self, frame_w: int, frame_h: int):
        # Zonas definidas como proporção do frame para ser independente de resolução
        self.zones: list[Zone] = [
            Zone(
                name="Nucleo de Controle",
                x1=int(frame_w * 0.0),
                y1=int(frame_h * 0.0),
                x2=int(frame_w * 0.35),
                y2=int(frame_h * 0.50),
                restricted=True,
            ),
            Zone(
                name="Reator de Energia",
                x1=int(frame_w * 0.65),
                y1=int(frame_h * 0.50),
                x2=int(frame_w * 1.0),
                y2=int(frame_h * 1.0),
                restricted=True,
            ),
            Zone(
                name="Area de Circulacao",
                x1=int(frame_w * 0.35),
                y1=int(frame_h * 0.0),
                x2=int(frame_w * 0.65),
                y2=int(frame_h * 1.0),
                restricted=False,
            ),
        ]

    def check_intrusion(self, boxes: list[tuple]) -> list[tuple[Zone, tuple]]:
        """
        Retorna lista de (Zone, box) para cada movimento detectado
        dentro de uma zona restrita.
        """
        intrusions = []
        for box in boxes:
            bx, by, bw, bh = box
            for zone in self.zones:
                if not zone.restricted:
                    continue
                # Checa sobreposição entre o box de movimento e a zona
                if (
                    bx < zone.x2
                    and bx + bw > zone.x1
                    and by < zone.y2
                    and by + bh > zone.y1
                ):
                    intrusions.append((zone, box))
                    break
        return intrusions

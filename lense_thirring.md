---
title: Analog of Lense -- Thirring effect in BEC
---

Notes about Lense -- Thirring project

## Hints
The french paper shows that a big vortex creates a Kerr metric, i.e. the one of a rotating Black hole, and that other vortices can act as test particles.

We would like to do the same, substituting the Kerr metric with the LT one.

NB we are still speaking of rotating bodies, but we go from a strong gravity limit (BH) to a weak limit, where the field is gravitomagnetic. Maybe a small vortex, i.e. a far away BH, can play the trick anyway.

what if the background density is the one of a vortex? do you get spinning black hole effects?

###  SOC
- Lense--Thirring precession --> rabi flop of some spinor

## TODO
- [ ] find the correct metric and try to imprint it in an empty universe. See what happens
  - [ ] run imaginary time. Do we get a stationary flow (= static gravitational field)?
- [ ] try to put a vortex on top of that and track the trajectory
  - [ ] describe it with geodesics
- [ ] send a wavepacket (HOW?)

## links
- <https://en.wikipedia.org/wiki/Lense%E2%80%93Thirring_precession>
- <https://arxiv.org/abs/1809.05386> [Solny] French paper that looks like the thing we want to do.
- <https://arxiv.org/abs/1510.01436> [Chak] Frame dragging effects in analogue gravity -- classical fluids
- <https://arxiv.org/abs/1207.2660> [Recati] A review by Alessio and friends, focusing on 1D BH and Hawking radiation
- <http://en.bookfi.net/book/1025099> The Universe in a Helium droplet: great book. See chap 31
- Pethick - Smith, chap 7

other articles, in vague order of importance

- <https://arxiv.org/abs/1410.2130> A recap about the Kerr metric

- <https://arxiv.org/abs/1705.05696> Analogue gravity in a *relativistc* BEC, by Luca Giacomelli =) maybe a bit too much
- <https://arxiv.org/abs/2001.03302> by Tapio Simula (nice name), vortices behave like massive particles in a gravitomagnetic field
- <https://arxiv.org/abs/0807.4910> Emergent gravity of massive phonons in a BEC
- <https://arxiv.org/abs/1911.03303> dipolar SOC BECs. Maybe I thought this could be relevant in Giulio's setup, where the analogue GM fiels arises form he spin orbit coupling.
- [A thesis from SISSA](https://iris.sissa.it/retrieve/handle/20.500.11767/3937/1625/1963_3767_Tesi_Sindoni_Definitiva.pdf)
- <https://academic.oup.com/mnras/article/423/3/2893/2461013> maybe neutron stars end up being super massive Bose–Einstein condensates (SMBEC)

### photon fluids
Do we need to go to BEC? Here, z propagation of the LG beam allows for a radial flow of the superfluid velocity, which means changing the r- dependance of the gravitomagnetic (GM) vector potential to something else other than 1/r. In a gas, this is the same as expanding the BEC

- <https://arxiv.org/abs/1704.07609> analogue gravity with an optical vortex. I'm sure we can do the same in a BEC
- <https://arxiv.org/abs/1908.00875> again, about photon fluid models. Here the metric has extra terms due to non-local interactions

## A bit of GR teminology
Write things down before forgetting them

[**de Sitter precession**](https://en.wikipedia.org/wiki/Geodetic_effect), or geometric precession, or geodetic effect. It's the precession of a vector carried around by an orbiting body around a central mass, i.e. in a curved spacetime. Part (?) of the effect can be described as [Thomas precession](https://en.wikipedia.org/wiki/Thomas_precession), which is the precession of a vector carried by an accelerating body in a flat spacetime. They're kinda the same effect, described in a unified way by the Fermi--Walker transport equation. See also [this discussion](https://physics.stackexchange.com/q/8043).

[**Lense--Thirring effect**](https://en.wikipedia.org/wiki/Lense%E2%80%93Thirring_precession), or frame-dragging effect, is an extra precession due to rotation of the central mass.

To see how the two things add up, look at the [Gravity probe B](https://en.wikipedia.org/wiki/Gravity_Probe_B) setup: the geodetic precession happens along the the orbit of the body, the frame-dragging one along the rotation plane of the primary body. In the GP-B, as it was along a polar orbit, the two effects were at right angles (NS and EW respectively) and could be separated. See <https://arxiv.org/abs/1105.3456> Fig.1

My problem is: WTF is preceding? The angular momentum of the body (e.g. if the satellite is spinning), but also (?) the plane of the orbit itself. In GP-B they measured the precession of gyroscopes, so the carried vector is the gyroscope angular momentum.

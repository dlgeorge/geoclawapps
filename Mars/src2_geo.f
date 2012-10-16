c
c
c =========================================================
      subroutine src2(maxmx,maxmy,meqn,mbc,mx,my,xlower,ylower,dx,dy,
     &             q,maux,aux,t,dt)
c =========================================================
      use geoclaw_module

      implicit double precision (a-h,o-z)

      dimension   q(1-mbc:maxmx+mbc,1-mbc:maxmy+mbc, meqn)
      dimension aux(1-mbc:maxmx+mbc,1-mbc:maxmy+mbc, maux)

      double precision source(2,10)
c

c     # incorporates friction using Manning coefficient

c      if (coeffmanning.eq.0.d0 .or. frictiondepth.eq.0) return

c     # check for NANs in solution:
c     call check4nans(maxmx,maxmy,meqn,mbc,mx,my,q,t,2)

      g=grav
      coeff = coeffmanning
      tol = 1.d-30  !# to prevent divide by zero in gamma

*     ! friction--------------------------------------------------------
      if (coeffmanning.gt.0.d0.and.frictiondepth.gt.0.d0) then
         do i=1,mx
            do j=1,my

               h=q(i,j,1)
               if (h.le.frictiondepth) then
c                 # apply friction source term only in shallower water
                  hu=q(i,j,2)
                  hv=q(i,j,3)

                  if (h.lt.tol) then
                     q(i,j,2)=0.d0
                     q(i,j,3)=0.d0
                  else
                     gamma= dsqrt(hu**2 + hv**2)*(g*coeff**2)/(h**(7/3))
                     dgamma=1.d0 + dt*gamma
                     q(i,j,2)= q(i,j,2)/dgamma
                     q(i,j,3)= q(i,j,3)/dgamma
                  endif
               endif
            enddo
         enddo
      endif
*     ! ----------------------------------------------------------------

*     ! coriolis--------------------------------------------------------
      if (icoordsys.eq.2.and.icoriolis.eq.1) then
         w = 2.d0*pi/(86400.d0) !angular velocity of earth
         do i=1,mx
            do j=1,my
               ycell = ylower + (j-.5d0)*dy
               cor = 2.d0*w*sin(pi*ycell/180.d0)
               ct = cor*dt
*              !integrate momentum exactly using matrix exponential
*              !forth order term should be sufficient since cor^3 ~= eps
               hu0 = q(i,j,2)
               hv0 = q(i,j,3)
*              !dq/dt = 2w*sin(latitude)*[0 1 ; -1 0] q = Aq
*              !e^Adt = [a11 a12; a21 a22] + I
               a11 = -0.5d0*ct**2 + ct**4/24.d0
               a12 = ct - ct**3/6.0d0
               a21 = -ct + ct**3/6.0d0
               a22 = a11
*              !q = e^Adt * q0
               q(i,j,2) = q(i,j,2) + hu0*a11 + hv0*a12
               q(i,j,3) = q(i,j,3) + hu0*a21 + hv0*a22
            enddo
         enddo
      endif
*     ! ----------------------------------------------------------------

      open(unit=77,file='../topo/mars_source_xy.dat',status='unknown')
      read(77,*) js
      do j=1,js
         read(77,*) source(1,j), source(2,j)
      enddo
      close(77)

      do i=1-mbc,mx+mbc
         x = xlower + (i-0.5d0)*dx
         do j=1-mbc,my+mbc
             y = ylower + (j-0.5d0)*dy
             q(i,j,1) = 0.d0
             do k = 1,js
               if ((source(1,k).gt.x-0.5d0*dx).and.
     &             (source(1,k).le.x+0.5d0*dx).and.
     &             (source(2,k).gt.y-0.5d0*dy).and.
     &             (source(2,k).le.y+0.5d0*dy)) then
                  q(i,j,1) = q(i,j,1) + dt*15.0/(dx*dy)
               endif
             enddo

             do m=2,meqn
               q(i,j,m)=0.d0
             enddo
         enddo
      enddo
c
      return
      end

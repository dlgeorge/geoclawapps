

c     =====================================================
       subroutine qinit(maxmx,maxmy,meqn,mbc,mx,my,xlower,ylower,
     &                   dx,dy,q,maux,aux)
c     =====================================================
c
c      # Set initial sea level flat unless mqinitfiles>0, in which case
c      # an initial perturbation of the q(i,j,iqinit) is specified and has
c      # been strored in qinitwork.


      use geoclaw_module
      use qinit_module

      implicit double precision (a-h,o-z)
      dimension q(1-mbc:maxmx+mbc, 1-mbc:maxmy+mbc, meqn)
      dimension aux(1-mbc:maxmx+mbc,1-mbc:maxmy+mbc,maux)

      double precision source(2,10)

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
                  write(*,*) 'qinit'
                  q(i,j,1) = 100.d0
               endif
             enddo

             do m=2,meqn
               q(i,j,m)=0.d0
             enddo
         enddo
      enddo
c
      xhigher = xlower + (mx-0.5d0)*dx
      yhigher = ylower + (my-0.5d0)*dy
c
      do mf =1,mqinitfiles

         if ((xlower.le.xhiqinit(mf).and.xhigher.ge.xlowqinit(mf)).and.
     &      (ylower.le.yhiqinit(mf).and.yhigher.ge.ylowqinit(mf))) then

            xintlow = dmax1(xlower,xlowqinit(mf))
            xinthi  = dmin1(xhigher,xhiqinit(mf))
            istart  = max(1-mbc,int(0.5 + (xintlow-xlower)/dx))
            iend    = min(mx+mbc,int(1.0 + (xinthi-xlower)/dx))

            yintlow = dmax1(ylower,ylowqinit(mf))
            yinthi  = dmin1(yhigher,yhiqinit(mf))
            jstart  = max(1-mbc,int(0.5 + (yintlow-ylower)/dy))
            jend    = min(my+mbc,int(1.0 + (yinthi-ylower)/dy))

            do i=istart,iend
               x = xlower + (i-0.5d0)*dx
               xim = x - 0.5d0*dx
               xip = x + 0.5d0*dx
               do j=jstart,jend
                  y = ylower + (j-0.5d0)*dy
                  yjm = y - 0.5d0*dy
                  yjp = y + 0.5d0*dy

                  if (xip.gt.xlowqinit(mf).and.xim.lt.xhiqinit(mf)
     &               .and.yjp.gt.ylowqinit(mf)
     &               .and.yjm.lt.yhiqinit(mf)) then

                     xipc=min(xip,xhiqinit(mf))
                     ximc=max(xim,xlowqinit(mf))
                     xc=0.5d0*(xipc+ximc)

                     yjpc=min(yjp,yhiqinit(mf))
                     yjmc=max(yjm,ylowqinit(mf))
                     yc=0.5d0*(yjmc+yjpc)

                     dq = topointegral(ximc,xc,xipc,yjmc,yc,yjpc,
     &                  xlowqinit(mf),ylowqinit(mf),
     &                  dxqinit(mf),dyqinit(mf),
     &                  mxqinit(mf),myqinit(mf),
     &                   qinitwork(i0qinit(mf):i0qinit(mf)+mqinit(mf)-1)
     &                     ,1)
                     dq=dq/((xipc-ximc)*(yjpc-yjmc)*aux(i,j,2))

                     if (iqinit(mf).le.meqn) then
                        q(i,j,iqinit(mf)) = q(i,j,iqinit(mf)) + dq
                     else
                        q(i,j,1) = max(dq-aux(i,j,1),0.d0)
                     endif
c
                  endif
c
               enddo
            enddo
         endif
      enddo

      return
      end

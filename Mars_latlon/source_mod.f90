!! ============================================================================
!  Program:     source_module
!  File:        source_mod.f90
!=======================================================================

module source_module

   implicit none

   double precision, allocatable :: source(:,:)
   integer :: isources

contains

    ! ========================================================================
    !  Reads in user parameters from the given file name if provided
    ! ========================================================================

   subroutine read_sourcefile(fname)

      implicit none

      ! Input
      character*35, intent(in), optional :: fname

      !Local
        integer, parameter :: iunit = 129
        integer :: j
        character*35 :: file_name
        logical :: found_file

        ! Read source parameters
        if (present(fname)) then
            file_name = fname
        else
            file_name = '../topo/src1_lonlat.dat'
        endif
        inquire(file=file_name,exist=found_file)
        if (.not. found_file) then
            print *, 'You must provide a file ', file_name
            stop
        endif

        if (.not.allocated(source)) then

            open(unit=iunit,file=file_name, status='unknown')

            read(iunit,*) isources
            allocate(source(2,isources))
            do j=1,isources
               read(iunit,*) source(1,j), source(2,j)
            enddo

            close(iunit)
         endif


   end subroutine read_sourcefile

end module source_module

<script lang="ts">
    import ChevronLeft from '$lib/components/icons/ChevronLeft.svelte';
    import ChevronRight from '$lib/components/icons/ChevronRight.svelte';
  
    export let pdfUrl: string = "./1d0963b0-f965-4a74-b445-f9c5fb8c749c_MOZZILLO_Missione_652_autoriz_dottorandi_signed_signed.pdf";
    export let isSidebarOpen: boolean = true;
  
    let pdfPath = pdfUrl.split('/').pop(); // Extract file name from the URL
    $: console.log('Sidebar is open:', isSidebarOpen); // Debugging
</script>
 
 
<div class="pdf-viewer-container">
    <div class="pdf-viewer">
      <iframe
        src={`/uploads/${pdfPath}`}
        type="application/pdf"
        class="w-full h-full pdf-iframe"
      ></iframe>
    </div>
  
    <div class="toggle-sidebar fixed-toggle" on:click={() => { isSidebarOpen = !isSidebarOpen; }}>
      {#if isSidebarOpen}
        <ChevronRight /> <!-- Icon when open -->
      {:else}
        <ChevronLeft /> <!-- Icon when closed -->
      {/if}
    </div>
  </div>
  
  <style>
    .pdf-viewer-container {
      display: flex;
      height: 100vh;
      background-color: #f5f5f5;
      position: relative;
    }
  
    .pdf-viewer {
      transition: width 0.3s ease; /* Smooth transition for the width change */
      width: 100%; /* Ensure the iframe takes full width */
    }
  
    .pdf-iframe {
      width: 100%;
      height: 100vh;
      border: none;
    }
  
    .toggle-sidebar.fixed-toggle {
      cursor: pointer;
      padding: 10px;
      background-color: #e0e0e0;
      border: 1px solid #ccc;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 40px;
      position: fixed;
      right: 0;
      top: 50%;
      transform: translateY(-50%);
      z-index: 2000; /* Increased z-index for visibility */
      border-radius: 8px 0 0 8px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }
  </style>
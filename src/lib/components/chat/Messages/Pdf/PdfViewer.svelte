<script lang="ts">
	export let pdfPath: string | undefined;
	export let isExpanded: boolean = false; // New prop to control the expanded state
</script>

{#if pdfPath}
	<div class="mt-4 w-full h-[500px] border rounded-xl overflow-hidden shadow-lg">
		<iframe
			src={`/uploads/${pdfPath}`}
			type="application/pdf"
			class="w-full h-full"
			style={isExpanded ? 'height: 100vh; width: 100vw;' : 'height: 500px;'}
		></iframe>
	</div>
{/if}
